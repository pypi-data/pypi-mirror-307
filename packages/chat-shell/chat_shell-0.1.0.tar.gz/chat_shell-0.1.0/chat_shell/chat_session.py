from datetime import datetime
import chat_shell.llm_model
from typing import List

class ChatSession:
    def __init__(self):
        # 存储对话历史
        self.conversation_history: List[dict] = [
            {"role": "system", "content": "You are a helpful assistant in a shell environment. "
             "You can see the user's shell commands and their outputs. "
             "When commenting on shell operations, be precise and helpful."}
        ]
    @staticmethod
    def create_pipeline_context(prompt: str, previous_output: str = None) -> List[dict]:
        """为管道创建独立的上下文"""
        context = [
            {"role": "system", "content": "您是shell管道中有用的助手。"
             "专注于处理当前输入并生成可传递给下一个命令的输出。 "
             }
        ]
        
        if previous_output is not None:
            context.append({
                "role": "user",
                "content": f"Previous pipeline output:\n{previous_output}\n\n 指令: {prompt} "
            })
        else:
            context.append({
                "role": "user",
                "content": prompt
            })
            
        return context
    def add_pipeline_context(self, pipeline_command: str, final_output: str, return_code: int):
        """将整个管道命令及其最终输出添加到全局上下文"""
        # 添加管道命令
        self.conversation_history.append({
            "role": "user",
            "content": f"[Pipeline Command at {datetime.now()}] {pipeline_command}"
        })
        
        # 添加最终输出
        self.conversation_history.append({
            "role": "assistant",
            "content": f"[Pipeline Output (return code: {return_code})]\n{final_output if final_output else 'No output'}"
        })
    def pipeline_chat(self, prompt: str, previous_output: str = None, is_first_chat: bool = False) -> str:
        """专门用于管道处理的chat方法"""
        try:
            if is_first_chat:
                # 第一个chat命令使用完整的会话历史
                self.conversation_history.append({
                    "role": "user",
                    "content": prompt
                })
                assistant_response = llm_model.chat_completions(self.conversation_history)
            else:
                # 后续chat命令使用独立上下文
                pipeline_context = self.create_pipeline_context(prompt, previous_output)
                assistant_response = llm_model.chat_completions(pipeline_context)
            
            return assistant_response
            
        except Exception as e:
            return f"Error in pipeline chat: {str(e)}"
    def add_shell_context(self, command: str, output: str, return_code: int):
        """添加shell命令和输出到对话历史，以对话形式"""
        # 添加用户的shell命令
        self.conversation_history.append({
            "role": "user",
            "content": f"[Shell Command at {datetime.now()}] {command}"
        })
        
        # 添加shell的响应
        response_content = f"[Shell Output (return code: {return_code})]\n{output if output else 'No output'}"
        self.conversation_history.append({
            "role": "assistant",
            "content": response_content
        })
        
    def chat(self, user_input: str) -> str:
        # 添加用户输入到对话历史
        self.conversation_history.append({
            "role": "user",
            "content": f"[Chat Question] {user_input}"
        })
        
        try:
            # 调用llm API
            # response = openai.ChatCompletion.create(
            #     model="llm",
            #     messages=self.conversation_history
            # )
            
            # 获取助手的回复
            assistant_response = llm_model.chat_completions(self.conversation_history)
            
            # 将助手的回复添加到对话历史
            self.conversation_history.append({
                "role": "assistant",
                "content": f"[Chat Response] {assistant_response}"
            })
            
            return assistant_response
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.conversation_history.append({
                "role": "assistant",
                "content": f"[Error] {error_msg}"
            })
            return error_msg
        
    def get_conversation_length(self) -> int:
        """获取对话历史长度"""
        return len(self.conversation_history)
    
    def trim_conversation_history(self, max_length: int = 20):
        """裁剪对话历史以防止过长"""
        if len(self.conversation_history) > max_length:
            # 保留系统消息和最近的对话
            self.conversation_history = [self.conversation_history[0]] + \
                                      self.conversation_history[-max_length+1:]
    
    def debug_history(self):
        """打印当前的对话历史（用于调试）"""
        for i, msg in enumerate(self.conversation_history):
            print(f"{i}. {msg['role']}: {msg['content']}\n")