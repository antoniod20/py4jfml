package jfml_entrypoint;

import jfml.FuzzyInferenceSystem;
import jfml.JFML;
import jfml.jaxb.FuzzySystemType;

/**
 * This class allows to return class instances of the JFML main package.
 *  
 */
public class JFML_Factory {
	
	public FuzzyInferenceSystem createFuzzyInferenceSystem() 
	{
		return new FuzzyInferenceSystem();
	}
	
	public FuzzyInferenceSystem createFuzzyInferenceSystem(String name) 
	{
		return new FuzzyInferenceSystem(name);
	}

	public FuzzyInferenceSystem createFuzzyInferenceSystem(FuzzySystemType fst) 
	{
		return new FuzzyInferenceSystem(fst);
	}
	
	public JFML createJFML() 
	{
		return new JFML();
	}
}
