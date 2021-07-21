import os
import sys
import re
import numpy
import torch
from transformers import XLMRobertaTokenizer, XLMRobertaConfig, XLMRobertaForSequenceClassification

# load tokenizer and pre-trained model
tokenizer = XLMRobertaTokenizer.from_pretrained('xlm-roberta-base', do_lower_case=True)
model_state_dict = torch.load('xlmr_model2.bin', map_location=torch.device('cpu'))
config = XLMRobertaConfig.from_pretrained('xlm-roberta-base', num_labels=3, output_hidden_states=False, output_attentions = False)
model = XLMRobertaForSequenceClassification.from_pretrained('xlm-roberta-base', config = config, state_dict = model_state_dict)
empty = {"Empty"}

def run(text_input):  
    # K.clear_session()

    REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
    REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    tex_input = REPLACE_NO_SPACE.sub("", text_input.lower())
    text_input = REPLACE_WITH_SPACE.sub(" ", text_input.lower())

    encoded_text = tokenizer.encode_plus(text_input, add_special_tokens=True, max_length=128, padding=True, return_attention_mask=True, 
                                            return_token_type_ids=True, return_tensors='pt')

    outputs = model(**encoded_text)

    output = outputs[0].detach().numpy()

    res = numpy.argmax(output)

    for i in range(3):
        if output[0][i] < 0:
            output[0][i] = 0

    sum = output[0][0] + output[0][1] + output[0][2]

    neg = round((output[0][0]*100)/sum, 2)
    pos = round((output[0][1]*100)/sum, 2)
    neutral = round((output[0][2]*100)/sum, 2)

    result = {'Positive' : pos, 'Negative' : neg, 'Neutral' : neutral}

    if res == 0:
        result['Result'] = 'Negative'
    elif res == 1:
        result['Result'] = 'Positive'
    else:
        result['Result'] = 'Neutral'

    return result