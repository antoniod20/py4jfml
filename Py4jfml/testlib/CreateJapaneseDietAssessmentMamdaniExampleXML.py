'''
This class creates an XML file with the definition of a Mamdani-type FLS for the Japanese Diet Assessment regression problem:
    1) Five input variables with Trapezoidal membership functions:
       + Percentage of Calories from Carbohydrate (PCC)
       + Percentage of Calories from Protein (PCP)
       + Percentage of Calories from Fat (PCF)
       + Percentage of Caloric Ratio (PCR)
       + Food Group Balance (FGB)

    2) Two rules
'''
from py4jfml.FuzzyInferenceSystem import FuzzyInferenceSystem
from py4jfml.Py4Jfml import Py4jfml
import os

from py4jfml.knowledgebase.KnowledgeBaseType import KnowledgeBaseType
from py4jfml.knowledgebasevariable.FuzzyVariableType import FuzzyVariableType
from py4jfml.rule.AntecedentType import AntecedentType
from py4jfml.rule.ClauseType import ClauseType
from py4jfml.rule.ConsequentType import ConsequentType
from py4jfml.rule.FuzzyRuleType import FuzzyRuleType
from py4jfml.rulebase.MamdaniRuleBaseType import MamdaniRuleBaseType
from py4jfml.term.FuzzyTermType import FuzzyTermType

japaneseDietAssessment = FuzzyInferenceSystem("japaneseDietAssessment - MAMDANI")

# KNOWLEDGE BASE
kb = KnowledgeBaseType()
japaneseDietAssessment.setKnowledgeBase(kb)

# FUZZY VARIABLE PCC(Percentage of Calories from Carbohydrate)
pcc = FuzzyVariableType("PCC", 0., 100.)

# FUZZY TERM low
pcc_low = FuzzyTermType("low", FuzzyTermType.TYPE_trapezoidShape,[0., 0., 55., 60.])
pcc.addFuzzyTerm(pcc_low)

# FUZZY TERM medium
pcc_medium = FuzzyTermType("medium", FuzzyTermType.TYPE_trapezoidShape,[55., 60., 65., 70.])
pcc.addFuzzyTerm(pcc_medium)

# FUZZY TERM high
pcc_high = FuzzyTermType("high", FuzzyTermType.TYPE_trapezoidShape,[65., 70., 100., 100.])
pcc.addFuzzyTerm(pcc_high)

kb.addVariable(pcc)

# FUZZY VARIABLE PCP(Percentage of Calories from Protein)
pcp = FuzzyVariableType("PCP", 0., 100.)

# FUZZY TERM low
pcp_low = FuzzyTermType("low", FuzzyTermType.TYPE_trapezoidShape,[0., 0., 10., 15.])
pcp.addFuzzyTerm(pcp_low)

# FUZZY TERM medium
pcp_medium = FuzzyTermType("medium", FuzzyTermType.TYPE_trapezoidShape,[10., 15., 18., 21.])
pcp.addFuzzyTerm(pcp_medium)


# FUZZY TERM high
pcp_high = FuzzyTermType("high", FuzzyTermType.TYPE_trapezoidShape,[18., 21., 100., 100.])
pcp.addFuzzyTerm(pcp_high)

kb.addVariable(pcp)

# FUZZY VARIABLE PCF(Percentage of Calories from Fat)
pcf = FuzzyVariableType("PCF", 0., 100.)

# FUZZY TERM low
pcf_low = FuzzyTermType("low", FuzzyTermType.TYPE_trapezoidShape,[0., 0., 15., 20.])
pcf.addFuzzyTerm(pcf_low)

# FUZZY TERM medium
pcf_medium = FuzzyTermType("medium", FuzzyTermType.TYPE_trapezoidShape,[15., 20., 24., 30.])
pcf.addFuzzyTerm(pcf_medium)

# FUZZY TERM high
pcf_high = FuzzyTermType("high", FuzzyTermType.TYPE_trapezoidShape, [24., 30., 100., 100.])
pcf.addFuzzyTerm(pcf_high)

kb.addVariable(pcf)

# FUZZY VARIABLE PCR(Percentage of Caloric Ratio)
pcr = FuzzyVariableType("PCR", 0., 200.)

# FUZZY TERM low
pcr_low = FuzzyTermType("low", FuzzyTermType.TYPE_trapezoidShape,[0., 0., 85., 95.])
pcr.addFuzzyTerm(pcr_low)

# FUZZY TERM medium
pcr_medium = FuzzyTermType("medium", FuzzyTermType.TYPE_trapezoidShape,[85., 95., 105., 115.])
pcr.addFuzzyTerm(pcr_medium)

# FUZZY TERM high
pcr_high = FuzzyTermType("high", FuzzyTermType.TYPE_trapezoidShape,[105., 115., 200., 200.])
pcr.addFuzzyTerm(pcr_high)

kb.addVariable(pcr)

# FUZZY VARIABLE FGB(Food Group Balance)
fgb = FuzzyVariableType("FGB", 0., 7.)

# FUZZY TERM low
fgb_low = FuzzyTermType("low", FuzzyTermType.TYPE_trapezoidShape,[0., 0., 1., 3.])
fgb.addFuzzyTerm(fgb_low)

# FUZZY TERM medium
fgb_medium = FuzzyTermType("medium", FuzzyTermType.TYPE_trapezoidShape,[1., 3., 4., 6.])
fgb.addFuzzyTerm(fgb_medium)

# FUZZYTERM high
fgb_high = FuzzyTermType("high", FuzzyTermType.TYPE_trapezoidShape,[4., 6., 7., 7.])
fgb.addFuzzyTerm(fgb_high)

kb.addVariable(fgb)

# FUZZY VARIABLE DHL(Dietary Healthy Level)
dhl = FuzzyVariableType("DHL", 0., 10.)
dhl.setDefaultValue(0.)
dhl.setAccumulation("MAX")
dhl.setDefuzzifierName("COG")
dhl.setType("output")

# FUZZY TERM very low
dhl_verylow = FuzzyTermType("very low", FuzzyTermType.TYPE_trapezoidShape,[0., 0., 1.5, 2.5])
dhl.addFuzzyTerm(dhl_verylow)

# FUZZY TERM low
dhl_low = FuzzyTermType("low", FuzzyTermType.TYPE_trapezoidShape,[1.5, 2.5, 3.5, 4.5])
dhl.addFuzzyTerm(dhl_low)

# FUZZY TERM medium
dhl_medium = FuzzyTermType("medium", FuzzyTermType.TYPE_trapezoidShape,[3.5, 4.5, 5.5, 6.5])
dhl.addFuzzyTerm(dhl_medium)

# FUZZY TERM high
dhl_high = FuzzyTermType("high", FuzzyTermType.TYPE_trapezoidShape,[5.5, 6.5, 7.5, 8.5])
dhl.addFuzzyTerm(dhl_high)

# FUZZY TERM high
dhl_veryhigh = FuzzyTermType("very high", FuzzyTermType.TYPE_trapezoidShape,[7.5, 8.5, 10., 10.])
dhl.addFuzzyTerm(dhl_veryhigh)

kb.addVariable(dhl)

# RULE BASE
rb = MamdaniRuleBaseType("rulebase1")

# RULE 1
r1 = FuzzyRuleType("rule1", connector="and", connectorMethod="MIN", weight=1.)
ant1 = AntecedentType()
ant1.addClause(ClauseType(pcc, pcc_low))
ant1.addClause(ClauseType(pcp, pcp_low))
ant1.addClause(ClauseType(pcf, pcf_low))
ant1.addClause(ClauseType(pcr, pcr_low))
ant1.addClause(ClauseType(fgb, fgb_low))
con1 = ConsequentType()
con1.addThenClause(variable=dhl, term=dhl_verylow)
r1.setAntecedent(ant1)
r1.setConsequent(con1)
rb.addRule(r1)

# RULE 243
r243 = FuzzyRuleType("rule243", connector="and", connectorMethod="MIN", weight=1.)
ant243 = AntecedentType()
ant243.addClause(ClauseType(pcc, pcc_high))
ant243.addClause(ClauseType(pcp, pcp_high))
ant243.addClause(ClauseType(pcf, pcf_high))
ant243.addClause(ClauseType(pcr, pcr_high))
ant243.addClause(ClauseType(fgb, fgb_high))
con243 = ConsequentType()
con243.addThenClause(variable=dhl, term=dhl_low)
r243.setAntecedent(ant243)
r243.setConsequent(con243)
rb.addRule(r243)

japaneseDietAssessment.addRuleBase(rb)

print(japaneseDietAssessment)

# WRITTING JAPANESE DIET ASSESSMENT EXAMPLE INTO AN XML FILE
japaneseDietAssessmentXMLFile = "JapaneseDietAssessmentMamdani.xml"
Py4jfml.writeFSTtoXML(japaneseDietAssessment, japaneseDietAssessmentXMLFile)

Py4jfml.kill()