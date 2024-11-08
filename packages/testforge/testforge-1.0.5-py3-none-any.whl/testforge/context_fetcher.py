import jedi
import ast
from pathlib import Path
from typing import Dict, Set, List, Tuple, Optional

class ContextFetcher:
    def __init__(self, project_path: str):
        """
        Initialize the code extractor with the root path of your project.

        Args:
            project_path: The root directory of your project
        """
        self.project_path = Path(project_path).resolve()

    def _get_function_node(self, source: str, function_name: str = None) -> Optional[ast.FunctionDef]:
        """
        Find the AST node for the specified function.
        If function_name is None, returns all function nodes.
        """
        tree = ast.parse(source)
        if function_name is None:
            return [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                return node
        return None

    def _get_class_node(self, source: str, class_name: str = None) -> Optional[ast.ClassDef]:
        """
        Find the AST node for the specified class.
        If class_name is None, returns all class nodes.
        """
        tree = ast.parse(source)
        if class_name is None:
            return [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                return node
        return None

    def _extract_node_code(self, source: str, node: ast.AST) -> str:
        """Extract the actual source code of any AST node using line numbers."""
        source_lines = source.splitlines()
        return '\n'.join(source_lines[node.lineno - 1:node.end_lineno])

    def _get_imports_from_file(self, file_path: str) -> List[str]:
        """Extract all import statements from a file."""
        with open(file_path, 'r') as f:
            source = f.read()

        imports = []
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append(f"import {name.name}")
            elif isinstance(node, ast.ImportFrom):
                names = [n.name for n in node.names]
                names_str = ', '.join(names)
                if node.module:
                    imports.append(f"from {node.module} import {names_str}")

        return imports

    def _get_definition_source(self, definition) -> Dict[str, str]:
        """
        Helper method to get the complete source code of a definition.
        Returns both the complete source and the file's content.
        """
        try:
            with open(definition.module_path, 'r') as f:
                file_content = f.read()

            if definition.type == 'function':
                node = self._get_function_node(file_content, definition.name)
            elif definition.type == 'class':
                node = self._get_class_node(file_content, definition.name)
            else:
                return None

            if node:
                return {
                    'complete_source': self._extract_node_code(file_content, node),
                    'file_content': file_content
                }
            return None
        except Exception as e:
            print(f"Warning: Could not get source for {definition.name}: {str(e)}")
            return None

    def _analyze_code_unit(self, script: jedi.Script, node: ast.AST, source: str) -> Dict:
        """
        Analyze a single code unit (function or class) and its dependencies.
        This is the shared logic between analyzing a single function and multiple functions.
        """
        names = script.get_names(all_scopes=True, definitions=True, references=True)

        # Filter to get only the names used within our target node
        unit_names = [
            name for name in names
            if hasattr(name, 'line') and
               name.line >= node.lineno and
               name.line <= node.end_lineno
        ]

        # Track dependencies and their locations
        dependencies = {}
        processed_files = set()
        required_imports = set()

        # Process each name found in the function
        for name in unit_names:
            if name.type in ('function', 'class'):
                definitions = name.goto()

                for definition in definitions:
                    if definition.module_path:
                        # Add to processed files to avoid duplicates
                        if definition.module_path not in processed_files:
                            processed_files.add(definition.module_path)
                            file_imports = self._get_imports_from_file(definition.module_path)
                            required_imports.update(file_imports)

                        if definition.type in ('function', 'class'):
                            module_name = definition.module_name or Path(definition.module_path).stem
                            full_name = f"{module_name}.{definition.name}"

                            source_info = self._get_definition_source(definition)

                            if source_info:
                                dependencies[full_name] = {
                                    'code': source_info['complete_source'],
                                    'file': definition.module_path.relative_to(self.project_path),
                                    'type': definition.type,
                                    'line': definition.line
                                }

        return {
            'code': self._extract_node_code(source, node),
            'dependencies': dependencies,
            'imports': required_imports
        }

    def get_function_info(self, file_path: str, function_name: str) -> Dict:
        """
        Extract function code and all its dependencies for a single function.
        """
        file_path = str(Path(file_path).resolve())

        with open(file_path, 'r') as f:
            source = f.read()

        function_node = self._get_function_node(source, function_name)
        if not function_node:
            raise ValueError(f"Function {function_name} not found in {file_path}")

        script = jedi.Script(path=file_path)
        result = self._analyze_code_unit(script, function_node, source)

        imports = sorted(list(result['imports']))
        imports.insert(0, Path(file_path).stem)
        return {
            'function_code': result['code'],
            'dependencies': result['dependencies'],
            'imports': imports
        }

    def get_file_info(self, file_path: str) -> Dict:
        """
        Extract information about all functions in a file and their dependencies.
        """
        file_path = str(Path(file_path).resolve())

        with open(file_path, 'r') as f:
            source = f.read()

        # Get all function nodes in the file
        function_nodes = self._get_function_node(source, None)

        script = jedi.Script(path=file_path)

        # Analyze each function
        functions = {}
        all_dependencies = {}
        all_imports = set()

        for node in function_nodes:
            result = self._analyze_code_unit(script, node, source)
            functions[node.name] = result['code']
            all_dependencies.update(result['dependencies'])
            all_imports.update(result['imports'])

        imports = sorted(list(all_imports))
        imports.insert(0, Path(file_path).stem)
        return {
            'functions': functions,
            'dependencies': all_dependencies,
            'imports': imports
        }
