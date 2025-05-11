
import openai

def get_next_skill_from_prompt(agent_name, memory, player_input):
    template_path = f"prompts/{agent_name}.txt"
    with open(template_path) as f:
        template = f.read()
    prompt = template.format(memory=memory, player_input=player_input)
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message['content'].strip()
