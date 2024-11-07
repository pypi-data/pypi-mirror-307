from dataclasses import dataclass


@dataclass
class PhasePrompt:
    demand_analysis: str = \
"""
As the {assistant_role}, to satisfy the new user's demand and the product should be realizable, \
first, we should discuss to decide which product modality do we want the product to be. \
Note that we MUST ONLY discuss the product modality and finish this discuss in 3 turns. \
Once we all have expressed our opinion(s) and agree with the results of the discussion unanimously, \
any of us MUST actively terminate the discussion by replying with only one line, \
which starts with a single symbol "<INFO>", followed by our final product modality, for example "<INFO> Application".
"""

    language_choose: str = \
"""
According to the new user's task and some creative brainstorm ideas listed below:
Task: {task}.
"Modality: {modality}.
Ideas: {ideas}.
We have decided to complete the task through a executable software implemented via a programming language. \
As the {assistant_role}, to satisfy the new user's demand and make the software realizable, you should propose a concrete programming language. \
If python can complete this task via Python, please answer Python; otherwise, answer another programming language (e.g., Java, C++, etc,). \
Note that we must "ONLY discuss the target programming language". \
Once we all have expressed our opinion(s) and agree with the results of the discussion unanimously, \
any of us must actively terminate the discussion and conclude the best programming language we have discussed without any other words or reasons, \
return only one line using the format: "<INFO> programming_language". \
For example: "<INFO> python".
"""

    coding: str = \
"""
According to the new user's task and our software designs listed below:  
Task: {task}. 
Task description: {description}. 
Modality: {modality}. 
Programming Language: {language} 
Ideas:{ideas} 
We have decided to complete the task through a executable software with multiple files implemented vi {language}. \
As the {assistant_role}, to satisfy the new user's demands, you should write one or multiple files \
and make sure that every detail of the architecture is, in the end, implemented as code. {gui} \
Think step by step and reason yourself to the right decisions to make sure we get it right. \
You will first lay out the names of the core classes, functions, methods that will be necessary, as w l as a quick comment on their purpose. \
Each file MUST strictly follow markdown code block format, \
where the following tokens must be replaced such that FILENAME is the lowercase file name including the file extension, \
LANGUAGE in the programming language, DOCSTRING is a string literal specified in source code \
that is used to document a specific segment of code, and CODE is the original code. You MUST put in format below:

FILENAME 
```LANGUAGE 
''' 
DOCSTRING 
''' 
CODE 
``` 

FILENAME2
```LANGUAGE 
''' 
DOCSTRING 
''' 
CODE 
``` 

FILENAME3
```LANGUAGE 
''' 
DOCSTRING 
''' 
CODE 
``` 

You will start with the main file, then go to the ones that are imported by that file, and so on. \
Please note that the code should be fully functional. Ensure to implement all functions. No placeholders (such as 'pass' in Python). \
When discuss finish, start with symbol "<INFO>"  and list all the codes in format above. Final output should be like:
"""

    code_complete: str = \
"""
According to the new user's task and our software designs listed below: 
Task: {task}. 
Modality: {modality}.
Programming Language: {language} 
Codes: {codes} 
Unimplemented File:

{unimplemented_file}

In our software, each file must strictly follow a markdown code block format, \
where the following tokens must be replaced such that FILENAME is the lowercase file name including the file extension, \
LANGUAGE in the programming language, \
DOCSTRING is a string literal specified in source code that is used to document a specific segment of code, \
and CODE is the original code You MUST put in format below:

FILENAME
```LANGUAGE
''' DOCSTRING
''' CODE
``` 

As the {assistant_role}, to satisfy the complete function of our developed software, you have to implement all methods \
in the {unimplemented_file} file which contains a unimplemented class. Now, implement all methods of the {unimplemented_file} \
You SHOULD NOT change the FILENAME(also case sensitive). FILENAME MUST included in answer. You MUST put updated code in format below:

FILENAME
```LANGUAGE
''' DOCSTRING
''' CODE
``` 

"""

    code_review_comment: str = \
"""
According to the new user's task and our software designs:
Task: {task}.
Modality: {modality}.
Programming Language: {language}
Ideas: {ideas}
Codes:
{codes}
As the {assistant_role}, to make the software directly operable without further coding, ChatDev have formulated the following regulations:
1) all referenced classes should be imported;
2) all methods should be implemented;
3) all methods need to have the necessary comments;
4) no potential bugs;
5) The entire project conforms to the tasks proposed by the user;
6) most importantly, do not only check the errors in the code, but also the logic of code. \
Make sure that user can interact with generated software without losing any feature in the requirement;
Now, you should check the above regulations one by one and review the codes in detail, \
propose one comment with the highest priority about the codes, and give me instructions on how to fix. \
Tell me your comment with the highest priority and corresponding suggestions on revision. \
If the codes are perfect and you have no comment on them, return only one line like "<INFO> Finished".
"""

    code_review_modification: str = \
"""
According to the new user's task, our designed product modality, languages and ideas, \
our developed first-edition source codes are listed below:
Task: {task}.
Modality: {modality}.
Programming Language: {language}
Ideas: {ideas}
Codes: 
{codes}
Comments on Codes:
{comments}
In the software, each file must strictly follow a markdown code block format, where the following tokens must be replaced \
such that FILENAME is the lowercase file name including the file extension, LANGUAGE in the programming language, \
DOCSTRING is a string literal specified in source code that is used to document a specific segment of code, and \
CODE is the original code. Format:
FILENAME
```LANGUAGE
'''
DOCSTRING
'''
CODE
```
As the {assistant_role}, to satisfy the new user's demand and make the software creative, executive and robust, \
you should modify corresponding codes according to the comments. \
Then, output the full and complete codes with all bugs fixed based on the comments. Return all codes strictly following the required format.
"""

    test_error_summary: str = \
"""
Our developed source codes and corresponding test reports are listed below:
Programming Language: {language}
Source Codes:
{codes}
Test Reports of Source Codes:
{test_reports}
According to my test reports, please locate and summarize the bugs that cause the problem.
"""

    test_modification: str = \
"""
Our developed source codes and corresponding test reports are listed below:
Programming Language: {language}
Source Codes:
{codes}
Test Reports of Source Codes:
{test_reports}
Error Summary of Test Reports:
{error_summary}
Note that each file must strictly follow a markdown code block format, where the following tokens must be replaced \
such that FILENAME is the lowercase file name including the file extension, \
LANGUAGE in the programming language, DOCSTRING is a string literal specified in source code that is used to document \
a specific segment of code, and CODE is the original code:
FILENAME
```LANGUAGE
'''
DOCSTRING
'''
CODE
```
As the {assistant_role}, to satisfy the new user's demand and make the software execute smoothly and robustly, \
you should modify the codes based on the error summary. Now, use the format exemplified above and modify the problematic codes based on the error summary. \
Output the codes that you fixed based on the test reported and corresponding explanations (strictly follow the format defined above, \
including FILENAME, LANGUAGE, DOCSTRING and CODE; incomplete TODO codes are strictly prohibited). If no bugs are reported, \
please return only one line like <INFO> Finished.
"""

    manual: str = \
"""
The new user's task, our developed codes and required dependencies are listed:
Task: {task}.
Modality: {modality}.
Programming Language: {language}
Ideas: {ideas}
Codes: 
{codes}
Requirements:
{requirements}
As the {assistant_role}, by using Markdown, you should write a README.md file which is a detailed user manual to use the software, \
including introducing main functions of the software, how to install environment dependencies and how to use/play it. For example:
README.md
```
# LangChain
Building applications with LLMs through composability
Looking for the JS/TS version? Check out LangChain.js.
**Production Support:** As you move your LangChains into production, we'd love to offer more comprehensive support.
Please fill out this form and we'll set up a dedicated support Slack channel.
## Quick Install
`pip install langchain`
or
`conda install langchain -c conda-forge`
## 🤔 What is this?
Large language models (LLMs) are emerging as a transformative technology, enabling developers to build applications that they previously could not. However, using these LLMs in isolation is often insufficient for creating a truly powerful app - the real power comes when you can combine them with other sources of computation or knowledge.
This library aims to assist in the development of those types of applications. Common examples of these applications include:
**❓ Question Answering over specific documents**
- Documentation
- End-to-end Example: Question Answering over Notion Database
**🤖 Agents**
- Documentation
- End-to-end Example: GPT+WolframAlpha
## 📖 Documentation
Please see [here](https://python.langchain.com) for full documentation on:
- Getting started (installation, setting up the environment, simple examples)
- How-To examples (demos, integrations, helper functions)
- Reference (full API docs)
- Resources (high-level explanation of core concepts)
```
"""
