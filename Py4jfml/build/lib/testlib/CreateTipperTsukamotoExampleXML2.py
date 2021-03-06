'''
This class creates an XML file with the definition of a Tsukamoto-type FLS for the Tipper ruleression problem:
 *   1) Two input variables (food and service) with Triangular, rightLinear, leftGaussian, gaussian and rightGaussian membership functions
 *   2) One output with monotone (z and rightGaussian) membership functions but also using PointSetMonotonicShapeType and MonotonicInterpolationMethodType in the definition of the fuzzy term "cheap"
 *   3) Three rules
'''
from py4jfml.FuzzyInferenceSystem import FuzzyInferenceSystem
from py4jfml.Py4Jfml import Py4jfml
import os

from py4jfml.enumeration.MonotonicInterpolationMethodType import MonotonicInterpolationMethodType
from py4jfml.knowledgebase.KnowledgeBaseType import KnowledgeBaseType
from py4jfml.knowledgebasevariable.FuzzyVariableType import FuzzyVariableType
from py4jfml.knowledgebasevariable.TsukamotoVariableType import TsukamotoVariableType
from py4jfml.membershipfunction.PointSetMonotonicShapeType import PointSetMonotonicShapeType
from py4jfml.membershipfunction.PointType import PointType
from py4jfml.rule.AntecedentType import AntecedentType
from py4jfml.rule.ClauseType import ClauseType
from py4jfml.rule.ConsequentType import ConsequentType
from py4jfml.rule.FuzzyRuleType import FuzzyRuleType
from py4jfml.rulebase.TsukamotoRuleBaseType import TsukamotoRuleBaseType
from py4jfml.term.FuzzyTermType import FuzzyTermType
from py4jfml.term.TsukamotoTermType import TsukamotoTermType

tipper = FuzzyInferenceSystem("tipper - TSUKAMOTO")

#KNOWLEDGE BASE
kb = KnowledgeBaseType()
tipper.setKnowledgeBase(kb)

#FUZZY VARIABLE food
food = FuzzyVariableType(name="food", domainLeft=0.0, domainRight=10.0)

#FUZZY TERM rancid
rancid = FuzzyTermType(name="rancid", type_java=FuzzyTermType.TYPE_triangularShape, param=[0.0, 2.0, 5.5])
food.addFuzzyTerm(rancid)

#FUZZY TERM delicious
delicious = FuzzyTermType(name="delicious", type_java=FuzzyTermType.TYPE_rightLinearShape, param=[5.5, 10.0])
food.addFuzzyTerm(delicious)

kb.addVariable(food)

#FUZZY VARIABLE service
service = FuzzyVariableType(name="service", domainLeft=0.0, domainRight=10.0)

#FUZZY TERM poor
poor = FuzzyTermType(name="poor", type_java=FuzzyTermType.TYPE_leftGaussianShape, param=[0.0, 2.0])
service.addFuzzyTerm(poor)

#FUZZY TERM good
good = FuzzyTermType(name="good", type_java=FuzzyTermType.TYPE_gaussianShape, param=[5.0, 4.0])
service.addFuzzyTerm(good)

#FUZZY TERM excellent
excellent = FuzzyTermType(name="excellent", type_java=FuzzyTermType.TYPE_rightGaussianShape, param=[10.0, 2.0])
service.addFuzzyTerm(excellent)
		
kb.addVariable(service)

#TSUKAMOTO VARIABLE tip
tip = TsukamotoVariableType(name="tip", domainLeft=0.0, domainRight=20.0)
tip.setDefaultValue(0.0)
tip.setCombination("WA")
tip.setType("output")

#TSUKAMOTO TERM cheap
points1 = [PointType(0.0, 1.0),PointType(1.0, 1.0),PointType(2.0, 0.6),PointType(3.0, 0.4),PointType(4.0, 0.0)]
psm = PointSetMonotonicShapeType(points=points1)
psm.setInterpolationMethod(MonotonicInterpolationMethodType.CUBIC)
cheap = TsukamotoTermType(name="cheap", psm=psm)
tip.addTsukamotoTerm(t=cheap)

#TSUKAMOTO TERM average
average = TsukamotoTermType(name="average", type_java=FuzzyTermType.TYPE_zShape, paramList=[5.0, 15.0])
tip.addTsukamotoTerm(t=average)

#TSUKAMOTO TERM generous
generous = TsukamotoTermType(name="generous", type_java=FuzzyTermType.TYPE_rightGaussianShape, paramList=[20.0, 10.0])
tip.addTsukamotoTerm(t=generous)

kb.addVariable(tip)

#RULE BASE
rb = TsukamotoRuleBaseType("rulebase1")

#RULE 1
rule1 = FuzzyRuleType(name="rule1", connector="or", connectorMethod="MAX", weight=1.0)
ant1 = AntecedentType()
ant1.addClause(c=ClauseType(food, rancid))
ant1.addClause(c=ClauseType(service, poor, "very"))
con1 = ConsequentType()
con1.addThenClause(variable=tip, term=cheap)
rule1.setAntecedent(ant1)
rule1.setConsequent(con1)

rb.addRule(rule1)

#RULE 2
rule2 = FuzzyRuleType(name="rule2", connector="or", connectorMethod="MAX", weight=1.0)
ant2 = AntecedentType()
ant2.addClause(c=ClauseType(service, good))
con2 = ConsequentType()
con2.addThenClause(variable=tip, term=average)
rule2.setAntecedent(ant2)
rule2.setConsequent(con2)

rb.addRule(rule2)

#RULE 3
rule3 = FuzzyRuleType(name="rule3", connector="or", connectorMethod="MAX", weight=1.0)
ant3 = AntecedentType()
ant3.addClause(c=ClauseType(service, excellent))
ant3.addClause(c=ClauseType(food, delicious))
con3 = ConsequentType()
con3.addThenClause(variable=tip, term=generous)
rule3.setAntecedent(ant3)
rule3.setConsequent(con3)

rb.addRule(rule3)

tipper.addRuleBase(rb)

#WRITTING TIPPER EXAMPLE INTO AN XML FILE
tipperXMLFile = "TipperTsukamoto2.xml"
Py4jfml.writeFSTtoXML(tipper, tipperXMLFile)

print(tipper)

Py4jfml.kill()