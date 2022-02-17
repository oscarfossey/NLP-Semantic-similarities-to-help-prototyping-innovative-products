# NLP-Semantic-similarities-to-help-prototyping-innovative-products

*Oscar FOSSEY (LCPI, France), Frédéric Segonds (LCPI, France), Romain Pinquié (GSCOP, France)*

***This code has to be linked with [the paper](https://github.com/oscarfossey/NLP-Semantic-similarities-to-help-prototyping-innovative-products/blob/main/DREAM%20project%20LCPI%20Fossey/Paper%20and%20Video%20of%20presentation/Design%20Rules%20Extractor%20for%20Additive%20Manufacturability%20-%20Oscar%20Fossey.pdf) of Oscar Fossey : Design Rules Extractor for Additive Manufacturability (DREAM)***

**Oscar Fossey** is a research student at Arts et Metiers Institute of Technologie and 
member of the Product Design and Innovation Laboratory (LCPI). His research 
consists in using data analysis methods and tools for product design and 
innovation.

**Frédéric Segonds** is an Assistant Professor at Arts et Metiers Institute of 
Technologie and member of the Product Design and Innovation Laboratory 
(LCPI). His research interests focus on the early stages of design collaboration, 
optimization PLM and collaborative design. This area includes the integration of 
stakeholders’ core competences into the early stages of design and providing 
methodologies and tools to support early product design. 

**Romain Pinquié** is an Assistant Professor at the Grenoble Institute of Technology 
(Grenoble INP). He received a PhD in product design from Arts et Métiers 
Institute of Technology and an MSc in Computational and Software Techniques 
in Engineering, specialising in Computer-Aided Engineering from Cranfield 
University. His research at G-SCOP UMR CNRS concentrates on systems 
engineering, combining aspects of engineering design, modelling and simulation, 
data science, and virtual reality.


## GOAL of the tool ##
Looking for semantic similarities between textual descriptions of an innovative product ideas and a set of design rules to prototype parts with additive manufacturing. 

## Motivation ##

A large part of the designers/engineers who want to prototype their innovative ideas use additive manufacturing. However, a majority of them have little or no knowledge of the additive manufacturing techniques and their associated design rules. This can quickly become costly in time and resources. To solve this problem we have developed a DFAM tool to help designers/engineers who want to prototype their innovative ideas with additive manufacturing machines.

## Full design of the Dream tool: ##

![alt text](https://github.com/oscarfossey/NLP-Semantic-similarities-to-help-prototyping-innovative-products/blob/main/DREAM%20project%20LCPI%20Fossey/images/Ima%20dreamtool%20anglais.JPG)

## The different components : ##

The code is made of two modules and one text (a test text):

**DREAM :** The main module to match design rules and sentences of an idea sheet

**similarity_functions :**  
Module defining the main NLP functions using gensim,stanza and nltk:
- preprocessing the text 
- estimating the similarity score
- PDF to text function 
- blocnotes_ to text function


**Flow diagram and libraries used:**

![alt text](https://github.com/oscarfossey/NLP-Semantic-similarities-to-help-prototyping-innovative-products/blob/main/DREAM%20project%20LCPI%20Fossey/images/fluxofthecode.JPG)
![alt text](https://github.com/oscarfossey/NLP-Semantic-similarities-to-help-prototyping-innovative-products/blob/main/DREAM%20project%20LCPI%20Fossey/images/usedlibraries.JPG)

## Results ##

We tested our code on the textual description of the following use case a circular peeler: 

![alt text](https://github.com/oscarfossey/NLP-Semantic-similarities-to-help-prototyping-innovative-products/blob/main/DREAM%20project%20LCPI%20Fossey/images/usecase.JPG)

**Visualizations of the output data :**

![alt text](https://github.com/oscarfossey/NLP-Semantic-similarities-to-help-prototyping-innovative-products/blob/main/DREAM%20project%20LCPI%20Fossey/images/Results%20on%20use%20case.JPG)

## Credits ##

The project has been made by Oscar Fossey.

And it has been lead by Fréderic Segonds (LCPI), Romain Pinquié (G-SCOP) and Oscar Fossey (LCPI).

The use case has been provided by the LCPI (Laboratoire conception de produits et innovation : http://lcpi.ensam.eu/cpi-page-accueil-112719.kjsp)
