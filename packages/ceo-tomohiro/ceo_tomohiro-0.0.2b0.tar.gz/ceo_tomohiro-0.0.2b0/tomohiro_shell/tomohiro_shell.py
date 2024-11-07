import logging
import sys
import time
from typing import Iterator

from ceo import get_openai_model
from ceo.prompt import AnalyserPrompt, ExecutorPrompt, IntrospectionPrompt
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessageChunk
from colorama import Fore, Style

from tomohiro import Tomohiro
from tomohiro.tomohiro import NAME

log = logging.getLogger('ceo')


def _print(text: str | Iterator[BaseMessageChunk]):
    if isinstance(text, str):
        if text.startswith('\n'):
            text = text[1:]
        if text.startswith('\r'):
            text = text[1:]
        text = text.replace('{', '')
        text = text.replace('}', '')
        text = text.replace('\n', '')
        text = text.replace('\r', '')
        text = f'{text} '
        print(text, end='', flush=True)
        return text
    else:
        res = str()
        for chunk in text:
            c = chunk.content
            if c not in ['\n', '\r', '{', '}']:
                time.sleep(0.02)
                print(c, end='', flush=True)
                res += c
        print(' ', end='', flush=True)
        res += ' '
        return res


class TomohiroShell(Tomohiro):
    def __init__(self, brain: BaseChatModel):
        super().__init__(brain=brain)

    def step_quiet(self) -> str:
        if self.act_count < len(self.schedule):
            analysing = AnalyserPrompt(
                query=self.query_by_step,
                prev_results=self.prev_results,
                action=self.schedule[self.act_count],
                ext_context=self.ext_context
            )
            action, params = analysing.invoke(self.model)
            executing = ExecutorPrompt(params=params, action=action, ext_context=self.ext_context)
            _print(executing.explain(self.model, True))
            result = executing.invoke(model=self.model)
            action_str = f'Action {self.act_count + 1}/{len(self.schedule)}: {result}'
            self.prev_results.append(action_str)
            self.act_count += 1
            log.debug(action_str)
            return action_str
        self.reposition()
        return ''

    def just_do_it(self) -> str | None:
        if not self.plan():
            return None
        for act_count in range(len(self.schedule)):
            self.step_quiet()
        response_iter = (IntrospectionPrompt(
            query=self.query_high_level,
            prev_results=self.prev_results,
            ext_context=self.ext_context).invoke(self.model, True))
        response = _print(response_iter)
        log.debug(f'Conclusion: {response}')
        self.reposition()
        return f'{self.name}: {response}'


def main():
    tomohiro = TomohiroShell(get_openai_model())
    query = str()
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            query += f'{arg} '
    if query == '':
        query = 'Introduce yourself by only using tool named "find_information_about_the_assistant".'
    try:
        print(f'{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}{NAME}: {Style.RESET_ALL}', flush=True, end='')
        tomohiro.assign(query).just_do_it()
    except KeyboardInterrupt:
        pass
    exit(0)


if __name__ == '__main__':
    main()
