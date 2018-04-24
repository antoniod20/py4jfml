import progettoPy4jfml.Py4jfml as fml
from py4j.java_gateway import JavaGateway

gateway = JavaGateway()

# FuzzyInference
iris = fml.FuzzyInferenceSystem("iris - MAMDANI")
# KnowledgeBase
kb = fml.KnowledgeBaseType()
iris.setKnowledgeBase(kb)

# FUZZY VARIABLE SepalLength
sl = fml.FuzzyVariableType("SepalLength", 4.3, 7.9)

# FUZZY TERM low
sl_low = fml.FuzzyTermType("low", fml.FuzzyTerm.TYPE_trapezoidShape, [4.3, 4.3, 5.019, 6.048])
sl.addFuzzyTerm(sl_low)
# FUZZY TERM  medium
sl_medium = fml.FuzzyTermType("medium", fml.FuzzyTerm.TYPE_triangularShape, [5.019, 6.048, 7.05])
sl.addFuzzyTerm(sl_medium)
# FUZZY TERM high
sl_high = fml.FuzzyTermType("high", fml.FuzzyTerm.TYPE_trapezoidShape, [6.048, 7.05, 7.9, 7.9])
sl.addFuzzyTerm(sl_high)
# FUZZY TERM NOT(low)
sl_not_low = fml.FuzzyTermType("NOT(low)", fml.FuzzyTerm.TYPE_trapezoidShape, [4.3, 4.3, 5.019, 6.048])
sl_not_low.setComplement("true");
sl.addFuzzyTerm(sl_not_low);

kb.addVariable(sl);

# FUZZY VARIABLE SepalWidth
sw = fml.FuzzyVariableType("SepalWidth", 2., 4.4)

# FUZZY TERM low
sw_low = fml.FuzzyTermType("low", fml.FuzzyTerm.TYPE_trapezoidShape, [2., 2., 2.585, 3.119])
sw.addFuzzyTerm(sw_low)
# FUZZY TERM medium
sw_medium = fml.FuzzyTermType("medium", fml.FuzzyTerm.TYPE_triangularShape, [2.585, 3.119, 3.758])
sw.addFuzzyTerm(sw_medium)
# FUZZY TERM high
sw_high = fml.FuzzyTermType("high", fml.FuzzyTerm.TYPE_trapezoidShape, [3.119, 3.758, 4.4, 4.4])
sw.addFuzzyTerm(sw_high)
# FUZZY TERM NOT(high)
sw_not_high = fml.FuzzyTermType("NOT(high)", fml.FuzzyTerm.TYPE_trapezoidShape, [3.119, 3.758, 4.4, 4.4])
sw_not_high.setComplement("true")
sw.addFuzzyTerm(sw_not_high)

kb.addVariable(sw)

# FUZZY VARIABLE PetalLength
pl = fml.FuzzyVariableType("PetalLength", 1., 6.9)

# FUZZY TERM low
pl_low = fml.FuzzyTermType("low", fml.FuzzyTerm.TYPE_trapezoidShape, [1., 1., 1.464, 4.432])
pl.addFuzzyTerm(pl_low);
# FUZZY TERM medium
pl_medium = fml.FuzzyTermType("medium", fml.FuzzyTerm.TYPE_triangularShape, [1.464, 4.432, 5.826])
pl.addFuzzyTerm(pl_medium)
# FUZZY TERM high
pl_high = fml.FuzzyTermType("high", fml.FuzzyTerm.TYPE_trapezoidShape, [4.432, 5.826, 6.9, 6.9])
pl.addFuzzyTerm(pl_high)
# FUZZY TERM NOT(low)
pl_not_low = fml.FuzzyTermType("NOT(low)", fml.FuzzyTerm.TYPE_trapezoidShape, [1., 1., 1.464, 4.432])

pl_not_low.setComplement("true")
pl.addFuzzyTerm(pl_not_low)

kb.addVariable(pl)

# FUZZY VARIABLE PetalWidth
pw = fml.FuzzyVariableType("PetalWidth", 0.1, 2.5)

# FUZZY TERM low
pw_low = fml.FuzzyTermType("low", fml.FuzzyTerm.TYPE_trapezoidShape, [0., 0.1, 0.244, 1.337])
pw.addFuzzyTerm(pw_low)
# FUZZY TERM medium
pw_medium = fml.FuzzyTermType("medium", fml.FuzzyTerm.TYPE_triangularShape, [0.244, 1.337, 2.074])
pw.addFuzzyTerm(pw_medium)
# FUZZY TERM high
pw_high = fml.FuzzyTermType("high", fml.FuzzyTerm.TYPE_trapezoidShape, [1.337, 2.074, 2.5, 2.5])
pw.addFuzzyTerm(pw_high)

kb.addVariable(pw)

# OUTPUT CLASS irisClass
irisClass = fml.FuzzyVariableType("irisClass", 1., 3.)
irisClass.setDefaultValue(1.)
irisClass.setAccumulation("MAX")
irisClass.setDefuzzifierName("LM")
irisClass.setType("output")

# FUZZY TERM setosa
irisClass_setosa = fml.FuzzyTermType("setosa", fml.FuzzyTerm.TYPE_singletonShape, [1.])
irisClass.addFuzzyTerm(irisClass_setosa);

# FUZZY TERM virginica
irisClass_virginica = fml.FuzzyTermType("virginica", fml.FuzzyTerm.TYPE_singletonShape, [2.])
irisClass.addFuzzyTerm(irisClass_virginica)

# FUZZY TERM versicolor
irisClass_versicolor = fml.FuzzyTermType("versicolor", fml.FuzzyTerm.TYPE_singletonShape, [3.])
irisClass.addFuzzyTerm(irisClass_versicolor)

kb.addVariable(irisClass)

# RULE BASE
rb = fml.MamdaniRuleBaseType("rulebase-iris")
# RULE 1
r1 = fml.FuzzyRuleType("rule1", "and", "MIN", 1.0)

ant1 = fml.AntecedentType()
ant1.addClause(fml.ClauseType(pw, pw_low))
con1 = fml.ConsequentType()
con1.addThenClause(fml.ClauseType(irisClass, irisClass_setosa))
r1.setAntecedent(ant1)
r1.setConsequent(con1)

rb.addRule(r1)

# RULE 2
r2 = fml.FuzzyRuleType("rule2", "and", "MIN", 1.0)

ant2 = fml.AntecedentType()
ant2.addClause(fml.ClauseType(sw, sw_not_high))
ant2.addClause(fml.ClauseType(pl, pl_medium))
ant2.addClause(fml.ClauseType(pw, pw_medium))
con2 = fml.ConsequentType()
con2.addThenClause(fml.ClauseType(irisClass, irisClass_virginica))
r2.setAntecedent(ant2)
r2.setConsequent(con2)

rb.addRule(r2);

# RULE 3
r3 = fml.FuzzyRuleType("rule3", "and", "MIN", 1.0)

ant3 = fml.AntecedentType()
ant3.addClause(fml.ClauseType(sl, sl_not_low))
ant3.addClause(fml.ClauseType(pl, pl_not_low))
ant3.addClause(fml.ClauseType(pw, pw_high))

con3 = fml.ConsequentType()
con3.addThenClause(fml.ClauseType(irisClass, irisClass_versicolor))
r3.setAntecedent(ant3)
r3.setConsequent(con3)

rb.addRule(r3)

iris.addRuleBase(rb)

# WRITTING IRIS EXAMPLE INTO AN XML FILE
str_xml = "C:\\Users\\andrea\\PycharmProjects\\untitled\\progettoPy4jfml\\XMLFiles\\IrisMamdani2.xml"
fml.PY4JFML.writeFSTtoXML(iris, str_xml)