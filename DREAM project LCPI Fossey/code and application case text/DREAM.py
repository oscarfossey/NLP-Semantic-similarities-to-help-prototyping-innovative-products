# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 13:53:20 2021

@author: Oscar Fossey

This code has to be linked we the paper of Oscar Fossey Design Rules Extractor for Additive Manufacturability (DREAM)
"""

"""
This module is the end of the process to modify an excel to identify the similarities between rules and chunks

"""

import similarity_functions as sim_func    #Importing NLP functions we made to work with chunk of text

Nsentbychunks = 1           #Number of sentences by chunk
similarity_treshold = 0.35  #If a similarity score is above this value we will make the associations

# we define some class to have many variables asssocitaed to one object


class Idea_sheet():
    
    """ An idea-sheet is made of a text some sentences and some chunks"""
    
    def __init__(self, letext):
        self.text = letext
        self.sentences = [sentence(senttokens) for senttokens in sim_func.preprocess(self.text)]  #preprocess the text and split the senteces
        self.chunks = sim_func.sentence_to_chunks(self.sentences, Nsentbychunks)        #Define the different chunks using Nsentbychunks

class sentence():
    
    """ A sentence is made of tokens and one expanded representation"""
    
    def __init__(self, thetokens):
        self.tokens = thetokens
        self.exp_representation = sim_func.expanded_representation(thetokens)  #Define the expanded representation

               
class Design_rule():
    
    """ A design tule is made od a name the text of the rule , the keywords of the DR and the expanded representation of the DR"""
    
    def __init__(self, therulename, theruleannotation):
        self.name = therulename
        self.text = theruleannotation
        self.keywords = sim_func.preprocess(self.text)[0]
        self.exp_representation = sim_func.expanded_representation(self.keywords)
  
""" We define the idea sheet assiacted to our application case the vegetable circular peeler"""

pdf_test = "test.pdf"
bn_test = "test_text.txt"
# idea_sheet_test = Idea_sheet(sim_func.pdf_to_text(lepdfpath)) 
idea_sheet_test = Idea_sheet(sim_func.blocnotes_to_text(bn_test)) 

"""We define our reduced set of rules"""

AM_Design_rules_set = [Design_rule("Thin_wall_rule","The thickness of the walls of the part must not be less than 0.8 .")
                       ,Design_rule("Max_part_size_rule","The overall length of the full part size should be less than 1000")
                       ,Design_rule("Min_bars_size_rule","A circular bar must be larger than 2 and a rectangular bar must be larger than 3")
                       ,Design_rule("Materials_rule","The prototype should be functional with only plastic or polymer features, any other materials can not be used.")
                       ,Design_rule("Small_holes_rule","Holes made on the part should not be too small, minimum 2 of diameter")]


def DREAM(Design_rules_set,idea_sheet):
    """This function take a set of rules and an idea sheet and return the differents reccommended desifnrules
    Each recommandation as : a similiraty score (float) , a DR name (string) , a DR text (string) , the trigger words (strings, words tha was responsible of the matching),
    and the sentences used (string)."""
    Recommended_DR = []
    for chunk in idea_sheet.chunks:
        chunkrepr = sim_func.chunk_representation(chunk)
        for design_rule in AM_Design_rules_set:
            L = sim_func.similarity(chunkrepr, design_rule.exp_representation)
            sim_score = L[0]
            trigger_words = L[1]
            # print(sim_score)
            if sim_score > similarity_treshold:
                sentences = []
                for sent in chunk:
                    sentences += sent.tokens
                Recommended_DR += [(sim_score, design_rule.name, design_rule.text, trigger_words,sentences,'')]
    return Recommended_DR

import tablib

def save_results_excel(excelfilename, data):
    """This function save the results data in an already existing excel (associated with excelfilename)
    The data must be the output from the DREAM function.
    This function put the differents hyper parameters in the excel to track your performance according to some hyper parameters"""
    
    dataset = tablib.Dataset()
    dataset.headers = ('Score','Rule','Rule annotation', 'Trigger words', 'Tokens used from the text')
    
    with open(excelfilename,'rb') as exf:
    
        dataset.load(exf, 'xlsx')
    
    dataset.append_separator('Number of sent by chunk = ' + str(Nsentbychunks) + ', Number of expanded words by token = ' + str(sim_func.wordsbytoken) + ', Similarity treshold = ' + str(similarity_treshold))
    
    for rule in data:
        dataset.append(rule)
        
    with open(excelfilename,'wb') as exf:
        
        exf.write(dataset.export('xlsx'))

