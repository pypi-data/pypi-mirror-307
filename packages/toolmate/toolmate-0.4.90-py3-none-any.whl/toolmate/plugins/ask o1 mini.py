"""
ToolMate AI Plugin - ask chatgpt

Ask ChatGPT for conversation only; no function calling

[TOOL_CALL]
"""


from toolmate import config, getDynamicTokens, print1
#from toolmate.utils.call_chatgpt import CallChatGPT
import copy

try:
    CallChatGPT.checkCompletion()

    def ask_o1_mini(function_args):
        config.stopSpinning()
        query = function_args.get("query") # required
        config.currentMessages[-1] = {"role": "user", "content": query}

        # read beta limitations at https://platform.openai.com/docs/guides/reasoning/beta-limitations
        chatMessages = useChatSystemMessage(copy.deepcopy(config.currentMessages))
        chatMessages = [i for i in chatMessages if not i.get("role", "") == "system"] # beta doesn't support system message
        completion = config.oai_client.chat.completions.create(
            model="o1-mini",
            messages=chatMessages,
            max_completion_tokens=65536,
        )
        config.toolTextOutput = completion.choices[0].message.content
        print1(config.toolTextOutput)
        return ""

    functionSignature = {
        "examples": [
            "Ask o1-mini",
        ],
        "name": "ask_o1_mini",
        "description": "Ask reasoning model o1-mini to chat or provide information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The original request in detail, including any supplementary information",
                },
            },
            "required": ["query"],
        },
    }

    config.addFunctionCall(signature=functionSignature, method=ask_o1_mini)
    config.inputSuggestions.append("Ask o1-mini: ")

except:
    print("Plugin `ask o1-mini` not enabled! Check if your OpenAI API key is valid!")