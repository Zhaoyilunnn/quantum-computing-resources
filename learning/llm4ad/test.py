import os
from llm4ad.task.optimization.online_bin_packing import OBPEvaluation
from llm4ad.tools.llm.llm_api_https import HttpsApi
from llm4ad.method.eoh import EoH, EoHProfiler

if __name__ == "__main__":
    with open(os.path.expanduser("~/.config/openai/api"), "r") as f:
        key = f.read().strip()
        if not key.startswith("sk-"):
            raise ValueError(
                "Invalid OpenAI API key format. It should start with 'sk-'."
            )

    llm = HttpsApi(
        host="api.openai.com",  # your host endpoint, e.g., api.openai.com, api.deepseek.com
        key=key,  # your OpenAI API key
        model="gpt-4o",
        timeout=20,
    )
    task = OBPEvaluation()
    method = EoH(
        llm=llm,
        profiler=EoHProfiler(log_dir="logs/eoh", log_style="simple"),
        evaluation=task,
        max_sample_nums=20,
        max_generations=10,
        pop_size=4,
        num_samplers=1,
        num_evaluators=1,
        debug_mode=False,
    )
    method.run()
