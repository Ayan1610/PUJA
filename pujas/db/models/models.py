from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from datetime import date


class QuestionSet(models.Model):
    questionset_id = fields.IntField(pk=True)
    questionset_name = fields.CharField(max_length=255)
    questionset_status = fields.BooleanField()
    questionset_created_on = fields.DatetimeField(auto_now_add=True)
    questionset_created_by = fields.IntField(null=False)
    
    class Meta:
        table = 'Question_Set'
        
QuestionSet_Pydantic = pydantic_model_creator(QuestionSet, name='QuestionSet')
QuestionSetIn_Pydantic = pydantic_model_creator(QuestionSet, name="QuestionSet", exclude_readonly=True)



class QuestionSetIn_Pydantic(BaseModel):
    questionset_id: int
    questionset_name: str
    questionset_created_by: str
    questionset_status : bool

class QuestionSetCreate(BaseModel):
    questionset_name: str
    questionset_status: bool
    questionset_created_by: int




class Questions(models.Model):
    questions_id = fields.IntField(pk=True)
    questions_set = fields.ForeignKeyField('models.QuestionSet', related_name='questions')
    questions_number = fields.IntField()
    questions_text = fields.CharField(max_length=255)
    questions_options = fields.JSONField() # delimiter semicolon 
    # questions_is_comment_answer = fields.TextField() # if C~ then comment , if A~ then answer
    # questions_correct_option = fields.IntField()
    # questions_weight_equation= fields.TextField()
    questions_status = fields.BooleanField(default= True)
    questions_created_on = fields.DatetimeField(auto_now_add=True)
    questions_created_by = fields.IntField(null=False)
    questions_updated_on = fields.DatetimeField(null=True)
    questions_updated_by = fields.IntField(null=True)
    reverse_scored = fields.BooleanField(default=False)
    
    
    class Meta:
        table = 'Questions'
        
Questions_Pydantic = pydantic_model_creator(Questions, name='Questions')
QuestionsIn_Pydantic = pydantic_model_creator(Questions, name="Questions", exclude_readonly=True)


class QuestionsIn_Pydantic(BaseModel):
    questions_id: int
    questions_set: int
    questions_number: int
    questions_text: str
    questions_options: Dict[str, str]
    questions_status : bool
    reverse_scored: bool
    questions_created_by: int

class QuestionCreate(BaseModel):
    questions_set:int
    questions_number: int
    questions_text: str
    questions_options: Dict[str, str]
    reverse_scored: bool
    questions_created_by: int
 



class Answers(models.Model):
    answers_id = fields.IntField(pk=True)
    question = fields.ForeignKeyField('models.Questions', related_name='answers')
    selected_option = fields.IntField()
    reverse_scored = fields.BooleanField()
    answers_created_on = fields.DatetimeField(auto_now_add=True)
    answers_user_id= fields.IntField()   # the user who provided the answer   

    class Meta:
        table = "answers"


Answers_Pydantic = pydantic_model_creator(Answers, name="Answers")
AnswersIn_Pydantic = pydantic_model_creator(Answers, name="Answers", exclude_readonly=True)


class AnswersIn_Pydantic(BaseModel):
    answers_id: int
    question_id: int
    selected_option: int
    reverse_scored: bool


class AnswerCreate(BaseModel):
    question_id: int
    selected_option: int
    reverse_scored: bool





# class QuizBatch (models.Model):
#     quiz_batch_id = fields.IntField(pk=True)
    
# #need to finish it



# class Score(models.Model):
#     score_id = fields.IntField(pk=True)
#     score_user_id = fields.IntField()
#     question_set = fields.ForeignKeyField('models.QuestionSet', related_name='scores')
#     question= fields.ForeignKeyField('models.Questions', related_name='scores')
#     answer = fields.ForeignKeyField('models.Answers', related_name='scores')
#     score = fields.IntField()
#     stress_level =  fields.CharField(max_length=255)
#     score_date_taken = fields.DatetimeField(auto_now_add=True)

#     class Meta:
#         table = 'Scores'
      
#### TO Calculate the SCORE we dont need the question_id or answer_id , we use the selected option
# of each question       
        

class Score(models.Model):
    score_id = fields.IntField(pk=True)
    score_user_id = fields.IntField()
    question_set = fields.ForeignKeyField('models.QuestionSet', related_name='scores')
    score = fields.IntField()
    stress_level = fields.CharField(max_length=255)
    score_date_taken = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'Scores'        
        
    
        
        
Score_Pydantic = pydantic_model_creator(Score, name='Score')
ScoreIn_Pydantic = pydantic_model_creator(Score, name='Score', exclude_readonly=True)



class ScoreIn_Pydantic(BaseModel):
    score_id: int
    score_user_id:int
    question_set: int
    score: int
    score_level : str
    
    
    

    
        
    


