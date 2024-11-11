from typing import Dict, Any, List
from ...components.components_base import BaseWorkflow
from ...core.project_manager import ProjectManager
from ...services.markdown_service import MarkdownService
from ...services.llm_service import LLMService
from ...services.progress_service import ProgressService
from ...utils.common_utils import image_to_base64
from ...utils.logger import get_logger

logger = get_logger(__name__)


class ProjectModificationWorkflow(BaseWorkflow):
    def __init__(self, project_manager: ProjectManager, progress_service: ProgressService, model_config: Dict[str, Any]):
        super().__init__()
        self.project_manager = project_manager
        self.llm_service = LLMService(project_manager.project_path, project_manager.config)
        self.markdown_service = MarkdownService(project_manager.project_path, project_manager.config.get('repoai_ignore_file'))
        self.progress_service = progress_service
        
        self.modification_task = self.project_manager.get_task("project_modification_task")(
            self.llm_service, 
            self.progress_service,
            model_config=model_config.get("project_modification_task", {})
        )
        self.file_edit_task = self.project_manager.get_task("file_edit_task")(
            self.llm_service,
            self.progress_service,
            model_config=model_config.get("file_edit_task", {})
        )

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.modification_task.execute(context)
        self.progress_service.save_progress("project_modification", context)
        return context
    
    def populate_context(self, context: Dict[str, Any], user_input: str=None, project_report: str=None, file_paths: List[str]=None, image_paths: List[str]=None) -> Dict[str, Any]:
        if user_input:
            context['user_input'] = user_input
        if project_report:
            context['project_report'] = project_report
        if file_paths:
            context['file_contexts'] = self._process_file_contexts(file_paths)
        if image_paths:
            context['image_contexts'] = self._process_image_contexts(image_paths)
        return context

    def _process_file_contexts(self, file_contexts: List[str]) -> List[Dict[str, str]]:
        processed_contexts = []
        for file_path in file_contexts:
            content = self.project_manager.read_file(file_path)
            if content:
                processed_contexts.append({
                    "file_path": file_path,
                    "content": content
                })
        return processed_contexts

    def _process_image_contexts(self, image_contexts: List[str]) -> List[Dict[str, Dict[str, str]]]:
        processed_contexts = []
        for image_path in image_contexts:
            processed_contexts.append({"image_url": {"url": image_to_base64(image_path)}})
        return processed_contexts

    def apply_modifications(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        modifications = context.get('modifications', [])
        operations = []
        diffs = []

        for mod in modifications:
            operation = mod['operation']
            file_path = self.project_manager.verify_and_correct_file_path(mod['file_path'])

            if operation == 'create':
                operations.append({
                    'operation': 'create_file',
                    'file_path': file_path,
                    'content': mod['content']
                })
            elif operation == 'edit':
                current_content = self.project_manager.read_file(file_path)
                edit_context = {
                    'file_path': file_path,
                    'current_content': current_content,
                    'edit_message': mod['content']
                }
                self.file_edit_task.execute(edit_context)
                new_content = edit_context['new_content']
                operations.append({
                    'operation': 'edit_file',
                    'file_path': file_path,
                    'content': new_content
                })
                diffs.append(self._generate_edit_diff(file_path, current_content, mod['content'], new_content))
            elif operation == 'delete':
                operations.append({
                    'operation': 'delete_file',
                    'file_path': file_path
                })
            elif operation == 'move':
                operations.append({
                    'operation': 'move_file',
                    'file_path': file_path,
                    'content': mod['new_path']
                })
        
        self.project_manager.batch_operations(operations)
        self.progress_service.clear_progress()

        return diffs

    def _generate_edit_diff(self, file_path: str, current_content: str, suggested_content: str, new_content: str) -> Dict[str, Any]:
        import difflib
        return {
            'operation': 'edit',
            'file_path': file_path,
            'diff': {
                'current_vs_suggested': list(difflib.unified_diff(
                    current_content.splitlines(),
                    suggested_content.splitlines(),
                    fromfile=f'{file_path} (current)',
                    tofile=f'{file_path} (suggested)',
                    lineterm=''
                )),
                'current_vs_new': list(difflib.unified_diff(
                    current_content.splitlines(),
                    new_content.splitlines(),
                    fromfile=f'{file_path} (current)',
                    tofile=f'{file_path} (new)',
                    lineterm=''
                ))
            }
        }

    def generate_project_report(self) -> str:
        return self.markdown_service.generate_markdown_compilation(
            f" "
        )

    def reset_chat(self) -> Dict[str, Any]:
        new_context = {}
        new_context['messages'] = []
        new_context['project_report'] = self.generate_project_report()
        self.progress_service.clear_progress()
        return new_context

    def resume_workflow(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if 'modifications' in context:
            diffs = self.apply_modifications(context)
            context['diffs'] = diffs
        return context