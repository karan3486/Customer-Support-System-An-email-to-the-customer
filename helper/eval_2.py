from openai import OpenAI
import os
client = OpenAI()
customer_msg = f"""
tell me about the smartx pro phone and the fotosnap camera, 
the dslr one. Also, what TVs or TV related products 
do you have?"""
product_info = f"""
First is the SmartX ProPhone. This phone features a 
6.1-inch display and 128GB of storage, allowing you to 
store all your photos and videos without worry. It also 
comes with a 12MP dual camera, letting you capture clearer 
and more vibrant photos. Additionally, it supports 5G 
connectivity, so you can enjoy faster internet speeds. 
The SmartX ProPhone is priced at $899.99 and comes with 
a one-year warranty.

The second product is the Fotosnap DSLR Camera. This camera 
boasts a 24.2MP sensor, allowing you to capture high-quality 
images. It also supports 1080p video recording, so you can 
shoot clear videos. The camera is equipped with a 3-inch LCD 
screen, making it easy to instantly view your photos and videos. 
Moreover, it supports interchangeable lenses, enabling you to 
adjust based on your shooting needs. The Fotosnap DSLR Camera 
is priced at $599.99, also with a one-year warranty.
"""
assistant_answer = f"""
    Of course! We have two products to introduce to you.

    First is the SmartX ProPhone. This phone features a 
    6.1-inch display and 128GB of storage, allowing you to 
    store all your photos and videos without worry. It also 
    comes with a 12MP dual camera, letting you capture clearer 
    and more vibrant photos. Additionally, it supports 5G 
    connectivity, so you can enjoy faster internet speeds. 
    The SmartX ProPhone is priced at $899.99 and comes with 
    a one-year warranty.

    The second product is the Fotosnap DSLR Camera. This camera 
    boasts a 24.2MP sensor, allowing you to capture high-quality 
    images. It also supports 1080p video recording, so you can 
    shoot clear videos. The camera is equipped with a 3-inch LCD 
    screen, making it easy to instantly view your photos and videos. 
    Moreover, it supports interchangeable lenses, enabling you to 
    adjust based on your shooting needs. The Fotosnap DSLR Camera 
    is priced at $599.99, also with a one-year warranty.

    Do you have any further questions about these two products?
    """

cust_prod_info = {
    'customer_msg': customer_msg,
    'context': product_info
}
def get_completion_from_messages(messages, model="gpt-3.5-turbo", 
            temperature=0, max_tokens=500):
    response_comment = client.chat.completions.create(
    model=model,
    messages=messages
    )
    return response_comment.choices[0].message.content

def eval_with_rubric(test_set, assistant_answer):

    cust_msg = test_set['customer_msg']
    context = test_set['context']
    completion = assistant_answer
    
    system_message = """\
    You are an assistant that evaluates how well 
    the customer service agent \
    answers a user question by looking at the context 
    that the customer service \
    agent is using to generate its response. 
    """

    user_message = f"""\
       You are evaluating a submitted answer to a question 
       based on the context \
       that the agent uses to answer the question.

    Here is the data:

    [BEGIN DATA]
    ************
    [Question]: {cust_msg}
    ************
    [Context]: {context}
    ************
    [Submission]: {completion}
    ************
    [END DATA]

    Compare the factual content of the submitted 
    answer with the context. \
    Ignore any differences in style, grammar, or punctuation.

    Answer the following questions:

        - Is the Assistant response based only on the context 
        provided? (Y or N)
        - Does the answer include information that is not provided 
        in the context? (Y or N)
        - Is there any disagreement between the response and the 
        context? (Y or N)
        - Count how many questions the user asked. (output a number)
        - For each question that the user asked, is there a 
        corresponding answer to it?
        Question 1: (Y or N)
        Question 2: (Y or N)
        ...
        Question N: (Y or N)
        - Of the number of questions asked, how many of these 
        questions were addressed by the answer? (output a number)
    """
    
    

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]

    response = get_completion_from_messages(messages)
    return response


# In[ ]:

# Perform the evaluation and print the results.
evaluation_output = eval_with_rubric(cust_prod_info, 
          assistant_answer)
print(evaluation_output)