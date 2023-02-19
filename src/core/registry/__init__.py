
from core.registry.personalities import register_personalities, get_default_personality, get_default_personality_prompt, get_personality, get_personality_prompt, get_personality_names
from core.registry.interpreters import register_interpreters, get_interpreter, get_interpreter_runner, get_interpreter_names, get_active_interpreter, set_active_interpreter, get_active_interpreter_runner
from core.registry.commands import register_commands, get_command, get_command_handler, get_command_names
from core.registry.slash_commands import register_slash_commands, get_slash_command, get_slash_command_handler, get_slash_command_names
