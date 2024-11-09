import base64
import requests
from IPython.display import Image, display
import os
import time
from openai import OpenAI
from openai import AssistantEventHandler
from typing_extensions import override
import base64
import httpx
import anthropic


class MultiModal:
    def __init__(self, model, system_prompt=None, user_prompt=None):
        self.model = model
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.init_prompt()

    def init_prompt(self):
        if self.system_prompt is None:
            self.system_prompt = "You are a helpful assistant who helps users to write a report related to images in Korean."
        if self.user_prompt is None:
            self.user_prompt = "Explain the images as an alternative text in Korean."

    # 이미지를 base64로 인코딩하는 함수 (URL)
    def encode_image_from_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            image_content = response.content
            if url.lower().endswith((".jpg", ".jpeg")):
                mime_type = "image/jpeg"
            elif url.lower().endswith(".png"):
                mime_type = "image/png"
            else:
                mime_type = "image/unknown"
            return f"data:{mime_type};base64,{base64.b64encode(image_content).decode('utf-8')}"
        else:
            raise Exception("Failed to download image")

    # 이미지를 base64로 인코딩하는 함수 (파일)
    def encode_image_from_file(self, file_path):
        with open(file_path, "rb") as image_file:
            image_content = image_file.read()
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext in [".jpg", ".jpeg"]:
                mime_type = "image/jpeg"
            elif file_ext == ".png":
                mime_type = "image/png"
            else:
                mime_type = "image/unknown"
            return f"data:{mime_type};base64,{base64.b64encode(image_content).decode('utf-8')}"

    # 이미지 경로에 따라 적절한 함수를 호출하는 함수
    def encode_image(self, image_path):
        if image_path.startswith("http://") or image_path.startswith("https://"):
            return self.encode_image_from_url(image_path)
        else:
            return self.encode_image_from_file(image_path)

    def display_image(self, encoded_image):
        display(Image(url=encoded_image))

    def create_messages(
        self, image_url, system_prompt=None, user_prompt=None, display_image=True
    ):
        encoded_image = self.encode_image(image_url)
        if display_image:
            self.display_image(encoded_image)

        system_prompt = (
            system_prompt if system_prompt is not None else self.system_prompt
        )

        user_prompt = user_prompt if user_prompt is not None else self.user_prompt

        # 인코딩된 이미지를 사용하여 다른 처리를 수행할 수 있습니다.
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"{encoded_image}"},
                    },
                ],
            },
        ]
        return messages

    def invoke(
        self, image_url, system_prompt=None, user_prompt=None, display_image=True
    ):
        messages = self.create_messages(
            image_url, system_prompt, user_prompt, display_image
        )
        response = self.model.invoke(messages)
        return response.content

    def batch(
        self,
        image_urls: list[str],
        system_prompts: list[str] = [],
        user_prompts: list[str] = [],
        display_image=False,
    ):
        messages = []
        for image_url, system_prompt, user_prompt in zip(
            image_urls, system_prompts, user_prompts
        ):
            message = self.create_messages(
                image_url, system_prompt, user_prompt, display_image
            )
            messages.append(message)
        response = self.model.batch(messages)
        return [r.content for r in response]

    def stream(
        self, image_url, system_prompt=None, user_prompt=None, display_image=True
    ):
        messages = self.create_messages(
            image_url, system_prompt, user_prompt, display_image
        )
        response = self.model.stream(messages)
        return response


class OpenAIStreamHandler(AssistantEventHandler):
    @override
    def on_text_delta(self, delta, snapshot):
        return delta.value


class OpenAIAssistant:
    """
    OpenAI 어시스턴트를 관리하는 클래스입니다.
    이 클래스는 OpenAI API를 사용하여 파일 업로드, 어시스턴트 생성, 대화 관리 등의 기능을 제공합니다.
    """

    def __init__(self, configs):
        """
        OpenAIAssistant 클래스의 생성자입니다.

        :param configs: 설정 정보를 담은 딕셔너리
        configs = {
            "OPENAI_API_KEY": "OPENAI_API_KEY",
            "instructions": "사용자 입력 RAG 프롬프트미 설정시 기본 값",
            "PROJECT_NAME": "PDF-RAG-TEST", # 프로젝트 이름
            "model_name": "gpt-4o", # openai 모델 이름
            "chunk_size": 1000, # 청크 크기
            "chunk_overlap": 100, # 청크 중복 크기
        }
        """
        self.client = OpenAI(api_key=configs["OPENAI_API_KEY"])
        self.model = configs.get("model_name", "gpt-4o")
        self.instructions = configs.get("instructions", "")
        self.project_name = configs.get("PROJECT_NAME", "PDF-RAG-TEST")
        self.chunk_size = configs.get("chunk_size", 800)
        self.chunk_overlap = configs.get("chunk_overlap", 400)

        self.messages = []
        self.thread_id = None

    def upload_file(self, filepath):
        """
        파일을 OpenAI 서버에 업로드합니다.

        :param filepath: 업로드할 파일의 경로
        :return: 업로드된 파일의 ID
        """
        file = self.client.files.create(file=open(filepath, "rb"), purpose="assistants")
        return file.id

    def create_new_assistant(self, file_ids):
        """
        새로운 어시스턴트를 생성합니다.

        :param file_ids: 어시스턴트에 연결할 파일 ID 리스트
        :return: 생성된 어시스턴트의 ID와 벡터 스토어의 ID
        """
        # 현재 사용 사례에는 파일 검색 도구만 관련이 있습니다
        tools = [{"type": "file_search"}]

        chunking_strategy = {
            "type": "static",
            "static": {
                "max_chunk_size_tokens": self.chunk_size,
                "chunk_overlap_tokens": self.chunk_overlap,
            },
        }

        # 벡터 스토어 생성
        vector_store = self.client.beta.vector_stores.create(
            name=self.project_name,
            file_ids=file_ids,
            chunking_strategy=chunking_strategy,
        )
        tool_resources = {"file_search": {"vector_store_ids": [vector_store.id]}}

        # 어시스턴트 생성
        assistant = self.client.beta.assistants.create(
            name=self.project_name,
            instructions=self.instructions,
            model=self.model,
            tools=tools,
            tool_resources=tool_resources,
        )
        assistant_id = assistant.id
        vector_id = vector_store.id
        return assistant_id, vector_id

    def setup_assistant(self, assistant_id):
        """
        어시스턴트 ID를 설정합니다.

        :param assistant_id: 설정할 어시스턴트 ID
        """
        self.assistant_id = assistant_id

    def setup_vectorstore(self, vector_id):
        """
        벡터 스토어 ID를 설정합니다.

        :param vector_id: 설정할 벡터 스토어 ID
        """
        self.vector_id = vector_id

    def _start_assistant_thread(self, prompt):
        """
        어시스턴트와의 대화 스레드를 시작합니다.

        :param prompt: 초기 프롬프트 메시지
        :return: 생성된 스레드의 ID
        """
        # 메시지 초기화
        self.messages = [{"role": "user", "content": prompt}]

        # 스레드 생성
        tool_resources = {"file_search": {"vector_store_ids": [self.vector_id]}}
        thread = self.client.beta.threads.create(
            messages=self.messages, tool_resources=tool_resources
        )

        return thread.id

    def _run_assistant(self, thread_id):
        """
        어시스턴트를 실행합니다.

        :param thread_id: 실행할 스레드의 ID
        :return: 실행된 작업의 ID
        """
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=self.assistant_id
        )
        return run.id

    def _check_run_status(self, thread_id, run_id):
        """
        실행 상태를 확인합니다.

        :param thread_id: 스레드 ID
        :param run_id: 실행 ID
        :return: 실행 상태
        """
        run = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        return run.status

    def _retrieve_thread_messages(self, thread_id):
        """
        스레드의 메시지를 검색합니다.

        :param thread_id: 검색할 스레드의 ID
        :return: 메시지 리스트
        """
        thread_messages = self.client.beta.threads.messages.list(thread_id)
        list_messages = thread_messages.data
        thread_messages = []
        for message in list_messages:
            obj = {}
            obj["content"] = message.content[0].text.value
            obj["role"] = message.role
            thread_messages.append(obj)
        return thread_messages[::-1]

    def _add_messages_to_thread(self, thread_id, user_message):
        """
        스레드에 새 메시지를 추가합니다.

        :param thread_id: 메시지를 추가할 스레드의 ID
        :param user_message: 추가할 사용자 메시지
        :return: 추가된 메시지 객체
        """
        thread_message = self.client.beta.threads.messages.create(
            thread_id, role="user", content=user_message
        )
        return thread_message

    def invoke(self, message):
        """
        어시스턴트에게 메시지를 보내고 응답을 받습니다.

        :param message: 보낼 메시지
        :return: 어시스턴트의 응답
        """
        if len(self.messages) == 0:
            self.thread_id = self._start_assistant_thread(message)
        else:
            self._add_messages_to_thread(self.thread_id, message)

        run_id = self._run_assistant(self.thread_id)
        while self._check_run_status(self.thread_id, run_id) != "completed":
            time.sleep(1)
        answer = self._retrieve_thread_messages(self.thread_id)
        return answer[-1]["content"]

    def stream(self, message):
        """
        어시스턴트에게 메시지를 보내고 응답을 스트림으로 받습니다.

        :param message: 보낼 메시지
        :return: 어시스턴트의 응답 스트림
        """
        if len(self.messages) == 0:
            self.thread_id = self._start_assistant_thread(message)
        else:
            self._add_messages_to_thread(self.thread_id, message)

        handler = OpenAIStreamHandler()

        with self.client.beta.threads.runs.stream(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
            instructions=self.instructions,
            event_handler=handler,
        ) as stream:
            for text in stream.text_deltas:
                yield text

    def list_chat_history(self):
        """
        대화 기록을 반환합니다.

        :return: 대화 기록 리스트
        """
        return self._retrieve_thread_messages(self.thread_id)

    def clear_chat_history(self):
        """
        대화 기록을 초기화합니다.
        """
        self.messages = []
        self.thread_id = None


class AnthropicPDFAssistant:
    """
    Anthropic 어시스턴트를 관리하는 클래스입니다.
    이 클래스는 Anthropic API를 사용하여 PDF 파일 처리, 메시지 생성 등의 기능을 제공합니다.
    """

    def __init__(
        self,
        configs,
        pdf_path,
        use_prompt_cache=False,
        system_prompt: str = None,
    ):
        """
        AnthropicAssistant 클래스의 생성자입니다.

        :param configs: 설정 정보를 담은 딕셔너리
        configs = {
            "ANTHROPIC_API_KEY": "your_api_key",
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 4096,
            "betas": ["pdfs-2024-09-25"]
        }
        :param pdf_path: PDF 파일의 URL 또는 로컬 파일 경로
        :param use_prompt_cache: 프롬프트 캐싱 사용 여부 (기본값: False)
        """
        self.client = anthropic.Anthropic(
            api_key=configs.get("ANTHROPIC_API_KEY", None)
        )
        self.model = configs.get("model", "claude-3-5-sonnet-20241022")
        self.max_tokens = configs.get("max_tokens", 4096)
        self.betas = configs.get("betas", ["pdfs-2024-09-25"])
        self.use_prompt_cache = use_prompt_cache
        self.pdf_data = self._encode_pdf(pdf_path)
        self.messages = []
        # RAG 시스템 프롬프트 입력
        _DEFAULT_RAG_INSTRUCTIONS = """You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        Answer in same language as the question."""
        self.system_prompt = system_prompt or _DEFAULT_RAG_INSTRUCTIONS

    def _encode_pdf(self, pdf_path):
        """
        PDF 파일을 base64로 인코딩합니다.

        :param pdf_path: PDF 파일의 URL 또는 로컬 파일 경로
        :return: base64로 인코딩된 PDF 데이터
        """
        if pdf_path.startswith(("http://", "https://")):
            # URL인 경우
            return base64.standard_b64encode(httpx.get(pdf_path).content).decode(
                "utf-8"
            )
        else:
            # 로컬 파일 경로인 경우
            with open(pdf_path, "rb") as f:
                return base64.standard_b64encode(f.read()).decode("utf-8")

    def add_new_pdf(self, pdf_path):
        """
        새로운 PDF 파일을 추가하고 기존 대화 내역을 초기화합니다.

        :param pdf_path: 새로운 PDF 파일의 URL 또는 로컬 파일 경로
        """
        self.pdf_data = self._encode_pdf(pdf_path)
        self.clear_chat_history()

    def invoke(self, query, token_info=False):
        """
        PDF 파일과 쿼리를 포함한 메시지를 생성합니다.

        :param query: 사용자 질문
        :param token_info: 토큰 사용량 정보 반환 여부 (기본값: False)
        :return: API 응답 내용
        """

        betas = self.betas.copy()
        document_content = {
            "type": "document",
            "source": {
                "type": "base64",
                "media_type": "application/pdf",
                "data": self.pdf_data,
            },
        }

        if self.use_prompt_cache:
            betas.append("prompt-caching-2024-07-31")
            document_content["cache_control"] = {"type": "ephemeral"}

        if token_info:
            betas.append("token-counting-2024-11-01")

        if len(self.messages) == 0:
            self.messages.append({"role": "user", "content": self.system_prompt})
            self.messages.append(
                {
                    "role": "user",
                    "content": [
                        document_content,
                        {"type": "text", "text": query},
                    ],
                }
            )
        else:
            self.messages.append(
                {
                    "role": "user",
                    "content": query,
                }
            )

        message = self.client.beta.messages.create(
            model=self.model,
            betas=betas,
            max_tokens=self.max_tokens,
            messages=self.messages,
        )

        self.messages.append({"role": "assistant", "content": message.content[0].text})

        if token_info:
            return {
                "content": message.content[0].text,
                "usage": message.usage,
            }
        else:
            return {
                "content": message.content[0].text,
                "usage": "",
            }

    def stream(self, query, token_info=False):
        """
        PDF 파일과 쿼리를 포함한 메시지를 생성합니다.

        :param query: 사용자 질문
        :param token_info: 토큰 사용량 정보 반환 여부 (기본값: False)
        :return: API 응답 내용
        """
        betas = self.betas.copy()
        document_content = {
            "type": "document",
            "source": {
                "type": "base64",
                "media_type": "application/pdf",
                "data": self.pdf_data,
            },
        }

        if self.use_prompt_cache:
            betas.append("prompt-caching-2024-07-31")
            document_content["cache_control"] = {"type": "ephemeral"}

        betas.append("token-counting-2024-11-01")

        if len(self.messages) == 0:
            self.messages.append({"role": "user", "content": self.system_prompt})
            self.messages.append(
                {
                    "role": "user",
                    "content": [
                        document_content,
                        {"type": "text", "text": query},
                    ],
                }
            )
        else:
            self.messages.append(
                {
                    "role": "user",
                    "content": query,
                }
            )

        message = self.client.beta.messages.create(
            model=self.model,
            betas=betas,
            max_tokens=self.max_tokens,
            messages=self.messages,
            stream=True,
        )

        full_response = ""
        for text in message:
            if text.type == "content_block_delta":
                full_response += text.delta.text
                yield {"content": text.delta.text, "type": "token"}
            elif token_info:
                if text.type == "message_start":
                    yield {
                        "content": text.message.usage,
                        "type": "usage",
                    }
                elif text.type == "message_delta":
                    yield {
                        "content": text.usage,
                        "type": "usage",
                    }

        self.messages.append({"role": "assistant", "content": full_response})

    def clear_chat_history(self):
        self.messages = []

    @staticmethod
    def pretty_token_usage(usage):
        """
        토큰 사용량을 예쁘게 포맷팅하여 문자열로 반환하는 함수

        Args:
            response: Anthropic API 응답 객체
        Returns:
            str: 포맷팅된 토큰 사용량 문자열
        """
        usage_stats = usage.__dict__
        result = []
        result.append("\n토큰 사용 통계")
        result.append("-" * 40)
        for key, value in usage_stats.items():
            formatted_key = key.replace("_", " ").title()
            result.append(f"{formatted_key:<30} : {value:,}")
        result.append("-" * 40)
        return "\n".join(result)
