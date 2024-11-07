from abc import ABC, abstractmethod


class BasePhaseRepository(ABC):
    @abstractmethod
    def chatting(
        self,
        env,
        task_prompt,
        phase_prompt,
        assistant_role_name,
        assistant_role_prompt,
        user_role_name,
        user_role_prompt,
        placeholders,
        chat_turn_limit,
    ):
        pass

    @abstractmethod
    def update_phase_states(self, env_states):
        pass

    @abstractmethod
    def update_env_states(self, env_states):
        pass
