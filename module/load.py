import os
import importlib
# Engine configuration
# Model: GPT, LLAMA, HUMAN, etc.
def load():
    LLM_MODEL = os.getenv("LLM_MODEL", os.getenv("OPENAI_API_MODEL", "gpt-3.5-turbo")).lower()

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    if not (LLM_MODEL.startswith("llama") or LLM_MODEL.startswith("human")):
        assert OPENAI_API_KEY, "\033[91m\033[1m" + "OPENAI_API_KEY environment variable is missing from .env" + "\033[0m\033[0m"

    # Table config
    RESULTS_STORE_NAME = os.getenv("RESULTS_STORE_NAME", os.getenv("TABLE_NAME", ""))
    assert RESULTS_STORE_NAME, "\033[91m\033[1m" + "RESULTS_STORE_NAME environment variable is missing from .env" + "\033[0m\033[0m"

    # Run configuration
    INSTANCE_NAME = os.getenv("INSTANCE_NAME", os.getenv("BABY_NAME", "BabyAGI"))
    COOPERATIVE_MODE = "none"
    JOIN_EXISTING_OBJECTIVE = False

    # Goal configuration
    OBJECTIVE = os.getenv("OBJECTIVE", "")
    INITIAL_TASK = os.getenv("INITIAL_TASK", os.getenv("FIRST_TASK", ""))

    # Model configuration
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.0))


    # Extensions support begin

    def can_import(module_name):
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            return False


    DOTENV_EXTENSIONS = os.getenv("DOTENV_EXTENSIONS", "").split(" ")

    # Command line arguments extension
    # Can override any of the above environment variables
    ENABLE_COMMAND_LINE_ARGS = (
            os.getenv("ENABLE_COMMAND_LINE_ARGS", "false").lower() == "true"
    )
    if ENABLE_COMMAND_LINE_ARGS:
        if can_import("extensions.argparseext"):
            from extensions.argparseext import parse_arguments

            OBJECTIVE, INITIAL_TASK, LLM_MODEL, DOTENV_EXTENSIONS, INSTANCE_NAME, COOPERATIVE_MODE, JOIN_EXISTING_OBJECTIVE = parse_arguments()

    # Human mode extension
    # Gives human input to babyagi
    if LLM_MODEL.startswith("human"):
        if can_import("extensions.human_mode"):
            from extensions.human_mode import user_input_await

    # Load additional environment variables for enabled extensions
    # TODO: This might override the following command line arguments as well:
    #    OBJECTIVE, INITIAL_TASK, LLM_MODEL, INSTANCE_NAME, COOPERATIVE_MODE, JOIN_EXISTING_OBJECTIVE
    if DOTENV_EXTENSIONS:
        if can_import("extensions.dotenvext"):
            from extensions.dotenvext import load_dotenv_extensions

            load_dotenv_extensions(DOTENV_EXTENSIONS)

    # TODO: There's still work to be done here to enable people to get
    # defaults from dotenv extensions, but also provide command line
    # arguments to override them

    # Extensions support end

    print("\033[95m\033[1m" + "\n*****CONFIGURATION*****\n" + "\033[0m\033[0m")
    print(f"Name  : {INSTANCE_NAME}")
    print(f"Mode  : {'alone' if COOPERATIVE_MODE in ['n', 'none'] else 'local' if COOPERATIVE_MODE in ['l', 'local'] else 'distributed' if COOPERATIVE_MODE in ['d', 'distributed'] else 'undefined'}")
    print(f"LLM   : {LLM_MODEL}")


    # Check if we know what we are doing
    assert OBJECTIVE, "\033[91m\033[1m" + "OBJECTIVE environment variable is missing from .env" + "\033[0m\033[0m"
    assert INITIAL_TASK, "\033[91m\033[1m" + "INITIAL_TASK environment variable is missing from .env" + "\033[0m\033[0m"

    LLAMA_MODEL_PATH = os.getenv("LLAMA_MODEL_PATH", "models/llama-13B/ggml-model.bin")
    if LLM_MODEL.startswith("gpt-4"):
        print(
            "\033[91m\033[1m"
            + "\n*****USING GPT-4. POTENTIALLY EXPENSIVE. MONITOR YOUR COSTS*****"
            + "\033[0m\033[0m"
        )

    if LLM_MODEL.startswith("human"):
        print(
            "\033[91m\033[1m"
            + "\n*****USING HUMAN INPUT*****"
            + "\033[0m\033[0m"
        )

    print("\033[94m\033[1m" + "\n*****OBJECTIVE*****\n" + "\033[0m\033[0m")
    print(f"{OBJECTIVE}")

    if not JOIN_EXISTING_OBJECTIVE:
        print("\033[93m\033[1m" + "\nInitial task:" + "\033[0m\033[0m" + f" {INITIAL_TASK}")
    else:
        print("\033[93m\033[1m" + f"\nJoining to help the objective" + "\033[0m\033[0m")
    # Task storage supporting only a single instance of BabyAGI
    if COOPERATIVE_MODE in ['l', 'local']:
        if can_import("extensions.ray_tasks"):
            import sys
            from pathlib import Path

            sys.path.append(str(Path(__file__).resolve().parent))
            from extensions.ray_tasks import CooperativeTaskListStorage

            tasks_storage = CooperativeTaskListStorage(OBJECTIVE)
            print("\nReplacing tasks storage: " + "\033[93m\033[1m" + "Ray" + "\033[0m\033[0m")
    elif COOPERATIVE_MODE in ['d', 'distributed']:
        pass


