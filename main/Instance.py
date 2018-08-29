'''
/***********************************************************************

	This file is part of KEEL-software, the Data Mining tool for regression,
	classification, clustering, pattern mining and so on.

	Copyright (C) 2004-2010

	F. Herrera (herrera@decsai.ugr.es)
    L. S谩nchez (luciano@uniovi.es)
    J. Alcal谩-Fdez (jalcala@decsai.ugr.es)
    S. Garc铆a (sglopez@ujaen.es)
    A. Fern谩ndez (alberto.fernandez@ujaen.es)
    J. Luengo (julianlm@decsai.ugr.es)

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see http://www.gnu.org/licenses/

**********************************************************************/
'''
'''
/**
 * <p>
 * <b>Instance</b>
 * </p>
 *
 * This class keeps all the information of an instance. It stores nominal, 
 * integer and real values read from the file (in KEEL format). Also, it 
 * provides a set of methods to get information about the instance.
 *
 * @author Albert Orriols Puig
 * @version keel0.1 
 */
'''
from main import Attribute;
from main import Attributes;
from main import InstanceSet;
from main import InstanceParser;
from main import ErrorInfo;
class Instance :

    '''
/////////////////////////////////////////////////////////////////////////////
////////////////ATTRIBUTES OF THE INSTANCE CLASS ///////////////////////////
/////////////////////////////////////////////////////////////////////////////

	/**
	 * It is a vector of vectors of size 'number of attributes' where all the nominal
	 * values will of the attributes be stored. In nominalValues[0] the input values
	 * are stored, and int nominalValues[1] the output values are stored.
	 */
'''
__nominalValues=[];

'''
	/**
	 * It is a vector of vector of size 'number of attributes' where all the nominal
	 * values will of the attributes be stored, but transformed to a integer value.
	 */
 '''

__intNominal=[];

'''
	 * The vector realValues is a vector of vectors of size 'number of attributes'
	 * where all the integer and real attributes values will be stored. In realValues[0]
	 * all the input attribute values will be stored, while in realValues[1], the
	 * outputs will be stored.
'''
__realValues=[];

'''
	 * It is a vector of vectors of 'number of attributes' size that stores whichs
	 * attributes are missing for the inputs and the outputs.
'''
__missingValues=[];

'''
 * Indicates if the instance belongs to a train BD
'''
isTrain=None;


# Indicates the number of input attributes per instance.

__numInputAttributes=0;


#Indicates the number of output attributes per instance.

__numOutputAttributes=0;

'''
 * Indicates the number of undefined attributes (that are neither
 * inputs or outputs
'''
__numUndefinedAttributes=0;


# It indicates if the instance has any missing value

__anyMissingValue=[];


#	The next attriubtes define the position in the arrays where each attribute is stored

'''
 * Input attributes location
'''
ATT_INPUT = 0;


# Output attributes location

ATT_OUTPUT = 1;


 #Non-defined direction attributes location

ATT_NONDEF = 2;

'''
/////////////////////////////////////////////////////////////////////////////
/////////////////// METHODS OF THE INSTANCE CLASS ///////////////////////////
/////////////////////////////////////////////////////////////////////////////

/**
 * It parses a new attribute line.
 * @param def is the line to be parsed.
 * @param _isTrain is a flag that indicates if the BD is for a train run.
 * @param instanceNum is the number of the current instance. It's used to
 * write error message with the maximum amount of information.
 */
 '''
def __init__(self,defStr, _isTrain,instanceNum) :
    currentClass = -1;
    #System.out.println ("Reading data: "+def);
    st  = str.split(defStr,","); #Separator: "," and " "

    initClassAttributes();
    isTrain  = _isTrain;

    count=0,
    inAttCount=0,
    outAttCount=0,
    indefCount=0,
    inputOutput = 0,
    curCount=0;
    while (st.hasMoreTokens()) :
        #Looking if the attribute is an input, an output or it's undefined
        att = st.nextToken().trim();
        curAt = Attributes.getAttribute(count);
        directionAttr=curAt.getDirectionAttribute();
        if (directionAttr==Attribute.INPUT):
            inputOutput = Instance.ATT_INPUT;
            inAttCount= + 1;
            curCount = inAttCount;

        elif (directionAttr==Attribute.OUTPUT):
            inputOutput = Instance.ATT_OUTPUT;
            if (curAt.getType() == Attribute.NOMINAL):
                currentClass = curAt.convertNominalValue(att);

                #System.out.println ( " The position of the current class "+ att +" is: "+ currentClass );
            outAttCount += 1;
            curCount = outAttCount;

        else:
            #Attribute not defined neither as input or output. So, it is not read.
            inputOutput = Instance.ATT_NONDEF;
            indefCount+=1;
            curCount = indefCount;


        #The attribute is defined. So, its value is processed, and the attributes definitions
        #are checked to detect inconsistencies or to redefine undefined traits.
        processReadValue(curAt,defStr, att, inputOutput, count, curCount, instanceNum);

        #Finally, the counter of read attributes is updated.
        count+=1;
        #end of the while

    #Checking if the instance doesn't have the same number of attributes than defined.
    if(count != Attributes.getNumAttributes()) :
        er = ErrorInfo(ErrorInfo.BadNumberOfValues, instanceNum, InstanceParser.lineCounter, 0, 0, isTrain,("Instance "+defStr+" has a different number of attributes than defined\n   > Number of attributes defined: "+Attributes.getNumAttributes()+"   > Number of attributes read:    "+count));
    InstanceSet.errorLogger.setError(er);

    #Compute the statistics
    if (isTrain==True):
        atts = Attributes.getInputAttributes();
        length= int(len(atts));
        for i in range(0,length):
            if(self.missingValues[Instance.ATT_INPUT][i]==False):

                if((atts[i].getType() == Attribute.NOMINAL) and (Attributes.getOutputNumAttributes() == 1)):
                    atts[i].increaseClassFrequency(currentClass, nominalValues[Instance.ATT_INPUT][i]);
                elif((atts[i].getType() == Attribute.INTEGER or atts[i].getType() == Attribute.REAL) and missingValues[Instance.ATT_INPUT][i]==False):
                    atts[i].addInMeanValue(currentClass, realValues[Instance.ATT_INPUT][i]);


#end Instance

'''
 * Creates a deep copy of the Instance
 * @param inst Original Instance to be copied
'''
def __init__(self,inst):
    self.isTrain = inst.isTrain;
    self.numInputAttributes = inst.numInputAttributes;
    self.numOutputAttributes = inst.numOutputAttributes;
    self.numUndefinedAttributes = inst.numUndefinedAttributes;

    self.anyMissingValue = list.copyOf(inst.anyMissingValue, inst.anyMissingValue.length);
                         #str[inst.nominalValues.length][];
    self.nominalValues = str[inst.nominalValues.length];
    for i in range(0,len(self.nominalValues)):
        self.nominalValues[i] = list.copyOf(inst.nominalValues[i],inst.nominalValues[i].length);
                            #int[inst.intNominalValues.length][];
    self.intNominalValues = int[inst.intNominalValues.length];
    for i in range(0,len(self.nominalValues)):
        self.intNominalValues[i] = list.copyOf(inst.intNominalValues[i],inst.intNominalValues[i].length);

                         #float[inst.realValues.length][];
    self.realValues = float[inst.realValues.length];
    for i in range(0,len(self.realValues)):
        self.realValues[i] = list.copyOf(inst.realValues[i],inst.realValues[i].length);

       #bool[inst.missingValues.length][];
    self.missingValues = bool[inst.missingValues.length];
    for i in range(0,len(self.missingValues)):
        self.missingValues[i] = list.copyOf(inst.missingValues[i],inst.missingValues[i].length);

'''
 * Creates an instance from a set of given values. It is supposed that the values
 * correspond to the current Attributes static definition or InstanceAttributes
 * non-static definition (it depends on the InstanceSet to which this new instance
 * will belong). If ats is null, we will use the Attributes static definiton. If not
 * the ats definition instead.
 * @param values A double array with the values (either real or nominals' index). Missing values are stored as Double.NaN
 * @param ats The definition of the attributes (optional, if null we use Attributes definition).
'''
def __init__(values,instanceAttrs):
    curAt=Attribute();
    allat=[];
    inOut=0,
    inInt=0;
    out=0;
    undef=0;

    #initialise structures
    anyMissingValue = bool[3];
    anyMissingValue[0] = False;
    anyMissingValue[1] = False;
    anyMissingValue[2] = False;
    if(instanceAttrs==None):
        numInputAttributes  = Attributes.getInputNumAttributes();
        numOutputAttributes = Attributes.getOutputNumAttributes();
        numUndefinedAttributes = Attributes.getNumAttributes() - (numInputAttributes+numOutputAttributes);
    else:
        numInputAttributes  = instanceAttrs.getInputNumAttributes();
        numOutputAttributes = instanceAttrs.getOutputNumAttributes();
        numUndefinedAttributes = instanceAttrs.getNumAttributes() - (numInputAttributes+numOutputAttributes);

    intNominalValues =  [];
    nominalValues =  [];
    realValues    =  [];
    missingValues = [];
    nominalValues[0]    = str[numInputAttributes];
    nominalValues[1]    = str[numOutputAttributes];
    nominalValues[2]    = str[numUndefinedAttributes];
    intNominalValues[0] = int[numInputAttributes];
    intNominalValues[1] = int[numOutputAttributes];
    intNominalValues[2] = int[numUndefinedAttributes];
    realValues[0]       = float[numInputAttributes];
    realValues[1]       = float[numOutputAttributes];
    realValues[2]       = float[numUndefinedAttributes];
    missingValues[0]    = float[numInputAttributes];
    missingValues[1]    = bool[numOutputAttributes];
    missingValues[2]    = bool[numUndefinedAttributes];

    for i in range(0,numInputAttributes) :
        missingValues[0][i]=False;
    for i in range(0,numOutputAttributes) :
        missingValues[1][i]=False;
    for i in range(0,numUndefinedAttributes):
        missingValues[2][i]=False;

    #take the correct set of Attributes
    if(instanceAttrs!=None):
        allat = instanceAttrs.getAttributes();
    else:
        allat = Attributes.getAttributes();

    #fill the data structures
    inInt = out = undef = 0;
    for i in range(0,len(values)):
        curAt = allat[i];
        inOut = 2;
        if(curAt.getDirectionAttribute()==Attribute.INPUT):
            inOut = 0;
        elif(curAt.getDirectionAttribute()==Attribute.OUTPUT):
            inOut = 1;

        #is it missing?
        if(float(values[i]).isNaN()==True):
            if(inOut==0):
                missingValues[inOut][inInt] = True;
                anyMissingValue[inOut] = True;
                inInt +=1;
            elif(inOut==1):
                missingValues[inOut][out] = True;
                anyMissingValue[inOut] = True;
                out+=1;
            else:
                missingValues[inOut][undef] = True;
                anyMissingValue[inOut] = True;
                undef+=1;

        elif((curAt.getType()==Attribute.NOMINAL)==False): #is numerical?
            if(inOut==0):
                realValues[inOut][inInt] = values[i];
                inInt+=1;
            elif(inOut==1):
                realValues[inOut][out] = values[i];
                out+=1;
            else:
                realValues[inOut][undef] = values[i];
                undef+=1;

        else :#is nominal

            if(inOut==0):
                intNominalValues[inOut][inInt] = int(values[i]);
                realValues[inOut][inInt] = values[i];
                nominalValues[inOut][inInt] = curAt.getNominalValue(int(values[i]));
                inInt+=1;
            elif(inOut==1):
                intNominalValues[inOut][out] = int(values[i]);
                realValues[inOut][out] = values[i];
                nominalValues[inOut][out] = curAt.getNominalValue(int(values[i]));
                out+=1;
            else:
                intNominalValues[inOut][undef] = int(values[i]);
                realValues[inOut][undef] = values[i];
                nominalValues[inOut][undef] = curAt.getNominalValue(int(values[i]));
                undef+=1;


'''
/**
 * It processes the read value for an attribute
 * @param curAtt is the current attribute (the value read is from this attribute)
 * @param def is the whole String
 * @param inOut is an integer that indicates if the attribute is an input or an output attribute
 * @param count is a counter of attributes.
 * @param curCount is an attribute counter relative to the inputs or the output. So, it indicates
 * that the attribute is the ith attribute of the input or the output.
 * @param instanceNum is the number of the current instance. It's needed to write output messages
 * with the maximum possible amount of information.
 */
 
 '''
def processReadValue(self,curAtt, defStr,  att,  inOut, count,  curCount,  instanceNum):
    #Checking if there is a missing value.
    if(att.equalsIgnoreCase("<null>") or att.equalsIgnoreCase("?")) :
        Attributes.hasMissing = True;
        self.missingValues[inOut][curCount]=True;
        self.anyMissingValue[inOut] = True;
        if (inOut == 1): #If the output is a missing value, an error is generated.
            er =  ErrorInfo (ErrorInfo.OutputMissingValue, instanceNum,
                             InstanceParser.lineCounter, curCount, Attribute.OUTPUT,
                             isTrain,
                             ("Output attribute "+count+" of "+defStr+" with missing value."));
            InstanceSet.errorLogger.setError(er);

    elif(Attributes.getAttribute(count).getType()==Attribute.INTEGER or Attributes.getAttribute(count).getType()==Attribute.REAL) :
        try :
            self.realValues[inOut][curCount]=float(att);
        except  self.NumberFormatException as e :
            er =  ErrorInfo(ErrorInfo.BadNumericValue, instanceNum, InstanceParser.lineCounter, curCount, Attribute.INPUT+inOut, isTrain,
                            ("Attribute "+count+" of "+defStr+" is not an integer or real value."));
        InstanceSet.errorLogger.setError(er);

        #Checking if the new train value exceedes the bounds definition in train. The condition
        #also checks if the attribute is defined (is an input or an output).
        if (isTrain and inOut != 2):
            if (curAtt.getFixedBounds() and (curAtt.isInBounds(realValues[inOut][curCount])==False)):
                er =  ErrorInfo(ErrorInfo.TrainNumberOutOfRange, instanceNum, InstanceParser.lineCounter, curCount, Attribute.INPUT+inOut, isTrain,
                                ("ERROR READING TRAIN FILE. Value "+realValues[inOut][curCount]+" read for a numeric attribute that is not in the bounds fixed in the attribute '"+curAtt.getName()+"' definition."));
            InstanceSet.errorLogger.setError(er);

            curAtt.enlargeBounds(self.realValues[inOut][curCount]);

        elif(inOut!=2): #In test mode
            self.realValues[inOut][curCount] = curAtt.rectifyValueInBounds(realValues[inOut][curCount]);

    elif(Attributes.getAttribute(count).getType()==Attribute.NOMINAL) :
        self.nominalValues[inOut][curCount]= att;
    #Testing special cases.
    if (isTrain and inOut!=2):
        if (curAtt.getFixedBounds() and curAtt.isNominalValue(self.__nominalValues[inOut][curCount])==False):
            er =  ErrorInfo(ErrorInfo.TrainNominalOutOfRange, instanceNum, InstanceParser.lineCounter, curCount, Attribute.INPUT+inOut, isTrain,("ERROR READING TRAIN FILE. Value '"+self.__nominalValues[inOut][curCount]+"' read for a nominal attribute that is not in the possible list of values fixed in the attribute '"+curAtt.getName()+"' definition."));
            InstanceSet.errorLogger.setError(er);

            curAtt.addNominalValue(self.nominalValues[inOut][curCount]);
        elif(inOut!=2):
            if (curAtt.addTestNominalValue(self.__nominalValues[inOut][curCount])):
                    er =  ErrorInfo(ErrorInfo.TestNominalOutOfRange, instanceNum, InstanceParser.lineCounter, curCount, Attribute.INPUT+inOut, isTrain,
                                    ("ERROR READING TEST FILE. Value '"+self.nominalValues[inOut][curCount]+"' read for a nominal attribute that is not in the possible list of values fixed in the attribute '"+curAtt.getName()+"' definition."));
                    InstanceSet.errorLogger.setError(er);


            if (inOut != -2):
                self.intNominalValues[inOut][curCount] = curAtt.convertNominalValue(self.__nominalValues[inOut][curCount]);
                self.realValues[inOut][curCount] = self.intNominalValues[inOut][curCount];

                #end processReadValue


 # It reserves all the memory necessary for this instance

def initClassAttributes():
    anyMissingValue = bool[3];
    anyMissingValue[0] = False;
    anyMissingValue[1] = False;
    anyMissingValue[2] = False;
    numInputAttributes  = Attributes.getInputNumAttributes();
    numOutputAttributes = Attributes.getOutputNumAttributes();
    numUndefinedAttributes = Attributes.getNumAttributes() - (numInputAttributes+numOutputAttributes);
    intNominalValues = [];
    nominalValues = [];
    realValues    = [];
    missingValues = [];
    nominalValues[0]    = str[numInputAttributes];
    nominalValues[1]    = str[numOutputAttributes];
    nominalValues[2]    = str[numUndefinedAttributes];
    intNominalValues[0] = int[numInputAttributes];
    intNominalValues[1] = int[numOutputAttributes];
    intNominalValues[2] = int[numUndefinedAttributes];
    realValues[0]       = float[numInputAttributes];
    realValues[1]       = float[numOutputAttributes];
    realValues[2]       = float[numUndefinedAttributes];
    missingValues[0]    = float[numInputAttributes];
    missingValues[1]    = float[numOutputAttributes];
    missingValues[2]    = float[numUndefinedAttributes];

    for i in range (0,numInputAttributes):
        missingValues[0][i]=False;
    for i in range(0,numOutputAttributes):
        missingValues[1][i]=False;

    for i in range(0,numUndefinedAttributes):
        missingValues[2][i]=False;

   #end initClassAttributes

'''
 * It prints the instance to the specified PrintWriter.
 * @param out is the PrintWriter where to print.
'''
def printInstance (self,outHere):
    outHere.print("    > Inputs: ");
    for i in range (0, self.numInputAttributes):
        attrType=Attributes.getInputAttribute(i).getType();

        if( attrType==Attribute.NOMINAL):
            outHere.print(self.nominalValues[Instance.ATT_INPUT][i]);

        elif(attrType==Attribute.INTEGER):
            outHere.print(self.realValues[Instance.ATT_INPUT][i]);

        elif(attrType== Attribute.REAL):
            outHere.print(self.realValues[Instance.ATT_INPUT][i]);

        outHere.print("\n    > Outputs: ");
    for i in range (0,self.numOutputAttributes):
        attrType=Attributes.getOutputAttribute(i).getType();

        if(attrType== Attribute.NOMINAL):
            outHere.print(self.nominalValues[Instance.ATT_OUTPUT][i]);

        elif(attrType== Attribute.INTEGER):
            outHere.print(self.realValues[Instance.ATT_OUTPUT][i]);

        elif(attrType== Attribute.REAL):
            outHere.print(self.realValues[Instance.ATT_OUTPUT][i]);

        outHere.print("\n    > Undefined: ");
    for i in range(0,self.__numUndefinedAttributes):
        attrType=Attributes.getOutputAttribute(i).getType();

        if(attrType== Attribute.NOMINAL):
            outHere.print(self.nominalValues[Instance.ATT_OUTPUT][i]);

        if(attrType==  Attribute.INTEGER):
            outHere.print(self.realValues[Instance.ATT_OUTPUT][i]);

        if(attrType==  Attribute.REAL):
            outHere.print(self.realValues[Instance.ATT_OUTPUT][i]);

#end print
'''
 * It prints the instance to the specified PrintWriter.
 * The attribtes order is the same as the one in the
 * original file.
 * @param out is the PrintWriter where to print.
'''
def printAsOriginal (out):
    inCount = 0,
    outCount = 0,
    undefCount=0,
    count=0;
    numAttributes = Attributes.getNumAttributes();
    for count in range (0, numAttributes):
        at = Attributes.getAttribute(count);
        directionAttr=at.getDirectionAttribute();

        if(directionAttr== Attribute.INPUT):
            printAttribute(out, Instance.ATT_INPUT,   inCount, at.getType());
            inCount+=1;

        elif(directionAttr ==  Attribute.OUTPUT):
            printAttribute(out, Instance.ATT_OUTPUT, outCount, at.getType());
            outCount+=1;

        elif( directionAttr == Attribute.DIR_NOT_DEF):
            printAttribute(out, Instance.ATT_NONDEF, undefCount, at.getType());
            undefCount+=1;

        if (count+1 <numAttributes) :
            out.print(",");


 #end printAsOriginal

 # Does print an attribute to a PrintWriter

def printAttribute(self,out, inOut, ct,type):

    if (self.missingValues[inOut][ct]):
        out.print("<null>");

    else:

        if(type== Attribute.NOMINAL):
            out.print(self.nominalValues[inOut][ct]);

        elif (type == Attribute.INTEGER):
            out.print(int(self.realValues[inOut][ct]));

        elif(type == Attribute.REAL):
             out.print(self.realValues[inOut][ct]);



#end printAttribute

'''
/**
 * It does print the instance information
 */
 
 '''
def printFunction (self):
    print("  > Inputs ("+self.numInputAttributes+"): ");
    for  i in range (0, self.numInputAttributes):
        if (self.missingValues[Instance.ATT_INPUT][i]):
            print("?");

        else:
            inputAttrType=Attributes.getInputAttribute(i).getType();
            if(inputAttrType==Attribute.NOMINAL):
                print(self.nominalValues[Instance.ATT_INPUT][i]);

            if(inputAttrType== Attribute.INTEGER):
                print(int(realValues[Instance.ATT_INPUT][i]));

            if(inputAttrType== Attribute.REAL):
                print(self.realValues[Instance.ATT_INPUT][i]);



        print("  ");

    print("  > Outputs ("+self.numOutputAttributes+"): ");
    for i in range (0,self.numOutputAttributes):
        if (self.missingValues[Instance.ATT_OUTPUT][i]):
            print("?");

        else:
            outputAttr=Attributes.getOutputAttribute(i).getType();
            if(outputAttr== Attribute.NOMINAL):
                print(self.nominalValues[Instance.ATT_OUTPUT][i]);

            elif(outputAttr== Attribute.INTEGER):
                print(int(self.realValues[Instance.ATT_OUTPUT][i]));

            elif(outputAttr==Attribute.REAL):
                print(self.realValues[Instance.ATT_OUTPUT][i]);

        print("  ");
    print("  > Undefined ("+self.__numUndefinedAttributes+"): ");
    for i in range(0, self.__numUndefinedAttributes):
        if(self.missingValues[Instance.ATT_NONDEF][i]):
            print("?");

        else:
            undefinedAttrType=Attributes.getUndefinedAttribute(i).getType();

            if(undefinedAttrType== Attribute.NOMINAL):
                print(self.__nominalValues[Instance.ATT_NONDEF][i]);
            elif(undefinedAttrType == Attribute.INTEGER):

                print(self.__realValues[Instance.ATT_NONDEF][i]);

            elif(undefinedAttrType == Attribute.REAL):
                 print(self.__realValues[Instance.ATT_NONDEF][i]);

    print("  ");

#end print


'''
/////////////////////////////////////////////////////////////////////////////
////////////////////////GET AND SET METHODS ////////////////////////////////
/////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////
//	Functions to get all the input attributes, or all the output attributes //
/////////////////////////////////////////////////////////////////////////////
'''
'''
 * Get Input Real Values
 * @return a double[] of size equal to the number of input attributes
 * with the values of real attributes. Positions of the vector that doesn't
 * correspond to a real attribute has no rellevant data.
'''
def getInputRealValues():
    return self.realValues[0];
#end getInputRealAttributes

'''
 * Get Input Nominal Values
 * @return a string[] of size equal to the number of input attributes
 * with the values of nominal attributes. Positions of the vector that
 * doesn't correspond to a nominal attribute has no rellevant data.
'''
def getInputNominalValues():
    return nominalValues[0];
#end getInputNominalValues

'''
 * Get Input Missing Values
 * @return a boolean[] of size equal to the number of input attributes.
 * A true value in the position i of a vector indicates that the ith
 * input value is not known.
'''
def getInputMissingValues():
    return self.missingValues[0];
#end getINputMissingValues


'''
 * Get Output Real Values
 * @return a double[] of size equal to the number of output attributes
 * with the values of real attributes. Positions of the vector that doesn't
 * correspond to a real attribute has no rellevant data.
'''
def getOutputRealValues(self):
    return self.realValues[1];
#end getOutputRealAttributes

'''
 * Get Output Nominal Values
 * @return a string[] of size equal to the number of Output attributes
 * with the values of nominal attributes. Positions of the vector that
 * doesn't correspond to a nominal attribute has no rellevant data.
'''
def getOutputNominalValues(self):
    return self.nominalValues[1];
#end getOutputNominalValues

'''
 * Get Output Missing Values
 * @return a boolean[] of size equal to the number of Output attributes.
 * A true value in the position i of a vector indicates that the ith
 * Output value is not known.
'''
def getOutputMissingValues(self):
    return self.missingValues[1];
#end getOutputMissingValues

'''

/////////////////////////////////////////////////////////////////////////////
//	Functions to get one term of an input or output attribute          //
/////////////////////////////////////////////////////////////////////////////


/**
 * Get Input Real Values
 * @return a double with the indicated real input value.
 */
 '''
def getInputRealValues(pos):
    return self.realValues[0][pos];
#end getInputRealAttributes


'''
 * Get Input Nominal Values
 * @return a string with the indicated nominal input value.
'''
def getInputNominalValues(pos):
    return self.nominalValues[0][pos];
#end getInputNominalValues


'''
 * It does return the input nominal value at the specified position. The
 * nominal value is returned as an integer.
 * @param pos is the position.
 * @return an int with the nominal value.
'''
def getInputNominalValuesInt(pos):
    return self.intNominalValues[0][pos];
#end getInputNominalValues


'''
 * It does return all the input nominal values.
 * @return an int with the nominal value.
'''
def getInputNominalValuesInt():
    return self.intNominalValues[0];
#end getInputNominalValues


'''
 * Get Input Missing Values
 * @return a boolean indicating if that input value is missing.
'''
def getInputMissingValues(pos):
    return self.missingValues[0][pos];
#end getINputMissingValues


'''
 * Get Output Real Values
 * @return a double with the indicated real output value.
'''
def getOutputRealValues(pos):
    return self.realValues[1][pos];
#end getOutputRealAttributes


'''
 * Get Output Nominal Values
 * @return a string with the indicated nominal output value.
'''
def getOutputNominalValues(pos):
    return self.nominalValues[1][pos];
#end getOutputNominalValues


'''
 * It does return the output value at the specified position
 * @param pos is the position.
 * @return an int with the nominal value.
'''
def getOutputNominalValuesInt(pos):
    return self.intNominalValues[1][pos];
#end getInputNominalValues

'''
 * It does return the output value at the specified position
 * @return an int with the nominal value.
'''
def getOutputNominalValuesInt():
    return self.intNominalValues[1];
#end getInputNominalValues


'''
 * Get Output Missing Values
 * @return a boolean indicating if that output value is missing.
'''
def  getOutputMissingValues(pos):
    return self.missingValues[1][pos];
#end getOutputMissingValues

'''

/////////////////////////////////////////////////////////////////////////////
//	Functions to get all the attributes in a double[]             //
/////////////////////////////////////////////////////////////////////////////


/**
 * It does return all the input values. Doesn't care the type of the attributes.
 * Nominal attributes are transformed to an integer, that is codified with a double.
 * And integer attributes are codified with a double to. So all the values are
 * returnes as doubles.
 * @return a double[] with all input values.
 */
 '''
def getAllInputValues():
    return self.realValues[0];
#end getAllInputValues


'''
 * It does return the normalized values in a double[]. It means that integers are
 * normalized o [0..N], reals to [0..1] and nominals are transformed to an integer
 * value between [0..N], where N is the number of values that this nominal can take.
 * In addition, missing values are represented with a -1 value.
'''
def getNormalizedInputValues():
    norm = float[self.realValues[0].length];
    for i in range (0, len(norm)):
        if (self.missingValues[0][i]==False):
            norm[i] = Attributes.getInputAttribute(i).normalizeValue(self.realValues[0][i]);
        else:
            norm[i] = -1.;

    return norm;
#end getNormalizedInputValues


'''
 * It does return the normalized values in a double[]. It means that integers are
 * normalized o [0..N], reals to [0..1] and nominals are transformed to an integer
 * value between [0..N], where N is the number of values that this nominal can take.
'''
def getNormalizedOutputValues():
    norm = float[self.realValues[1].length];
    for i in range(0, norm.length):
        if (self.missingValues[1][i]==False):
            norm[i] = Attributes.getOutputAttribute(i).normalizeValue(realValues[1][i]);
        else:
            norm[i] = -1.;

    return norm;
#end getNormalizedOutputValues

'''
/**
 * It does return all the output values. Doesn't care the type of the attributes.
 * Nominal attributes are transformed to an integer, that is codified with a double.
 * And integer attributes are codified with a double to. So all the values are
 * returnes as doubles.
 * @return a double[] with all output values.
 */
 '''
def getAllOutputValues():
    return self.realValues[1];
#end getAllOutputValues

'''



/////////////////////////////////////////////////////////////////////////////
//	Functions to set values to an instance                  //
/////////////////////////////////////////////////////////////////////////////

/**
 * It changes the attribute value. If it can't do that, it returns a false
 * value.
 * @param pos is the attribute that has to be changed
 * @param value is the new value
 * @return a boolean in false state if the update of the value can't have
 * been done.
 */
 '''
def setInputNumericValue(pos, value):
    at = Attribute(Attributes.getInputAttribute(pos));
    if (at.getType() == Attribute.NOMINAL) :
        return False;
    else:
        if (at.isInBounds(value)):
            self.realValues[0][pos] = value;
            self.missingValues[0][pos] = False;
            self.anyMissingValue[0] = False;
            for i in range(0, self.missingValues[0].length):
                self.anyMissingValue[0] |= self.missingValues[0][i];

        else :
            return False;

    return True;
#end setInputNumericValue

'''
/**
 * It changes the attribute value. If it can't do that, it returns a false
 * value.
 * @param pos is the attribute that has to be changed
 * @param value is the new value
 * @return a boolean in false state if the update of the value can't have
 * been done.
 */
 '''
def setOutputNumericValue( self,pos,  value):
    at = Attribute(Attributes.getOutputAttribute(pos));
    if (at.getType() == Attribute.NOMINAL) :
        return False;
    else:
        if (at.isInBounds(value)):
            self.__realValues[1][pos] = value;
            self.__missingValues[1][pos] = False;
            self.__anyMissingValue[1] = False;
            for i in range(0, len(self.__missingValues[1])):
                self.anyMissingValue[1] |= self.missingValues[1][i];

        else:
            return False;

    return True;
  # end setInputNumericValue
'''

/**
 * It set the nominal attribute value to the one passed.
 * @param pos is the position of the attribute.
 * @param value is the new value.
 * @return boolean set to false if the update has not been done.
 */
 '''
def setInputNominalValue( self,pos,  value):
    at = Attribute(Attributes.getInputAttribute(pos));
    if (at.getType() != Attribute.NOMINAL):
        return False;
    else:
        if (at.convertNominalValue(value) != -1):
            self.__nominalValues[0][pos] = value;
            self.__intNominalValues[0][pos] = at.convertNominalValue(value);
            self.__realValues[0][pos] = self.__intNominalValues[0][pos];
            self.__missingValues[0][pos] = False;
            self.__anyMissingValue[0] = False;
            for i in range(0,self.__missingValues[0].length):
                self.__anyMissingValue[0] |= self.__missingValues[0][i];

        else :
            return False;

    return True;
#end setInputNominalValue


'''
/**
 * It set the nominal attribute value to the one passed.
 * @param pos is the position of the attribute.
 * @param value is the new value.
 * @return boolean set to false if the update has not been done.
 */
'''
def setOutputNominalValue(self, pos,  value):
    at = Attribute(Attributes.getOutputAttribute(pos));
    if (at.getType() != Attribute.NOMINAL) :
        return False;
    else:
        if (at.convertNominalValue(value) != -1):
            self.nominalValues[1][pos] = value;
            self.intNominalValues[1][pos] = at.convertNominalValue(value);
            self.realValues[1][pos] = self.intNominalValues[0][pos];
            self.missingValues[1][pos] = False;
            self.anyMissingValue[1] = False;
            for  i in range(0,self.missingValues[1].length):
                self.anyMissingValue[1] |= self.missingValues[1][i];

        else :
            return False;

    return True;
#end setOutputNominalValue

'''
/////////////////////////////////////////////////////////////////////////////
//	General questions about the instance                 //
/////////////////////////////////////////////////////////////////////////////

/**
 * It returns if there is any missing value.
 * @return a boolean indicating if there's any missing value.
 */
 '''
def existsAnyMissingValue(self):
    return (self.__anyMissingValue[0] or self.__anyMissingValue[1]);
#end existsAnyMissingValue

'''
/**
 * It informs about the existence of missing values in the inputs
 * @return a boolean indicating if there's any missing value in the input
 */
 '''
def existsInputMissingValues(self):
    return self.__anyMissingValue[0];
#end existsInputMissingValues

'''
/**
 * It informs about the existence of missing values in the outputs.
 * @return a boolean indicating if there's any missing value in the outputs.
 */
 '''
def existsOutputMissingValues(self):
    return self.__anyMissingValue[1];
#end existsOutputMissingValues

'''
/////////////////////////////////////////////////////////////////////////////
//	Removing an attribute of the instance                 //
/////////////////////////////////////////////////////////////////////////////
/**
 * It does remove the values of one attribute of the instance.
 * @param attToDel is a reference to the attribute to be deleted.
 * @param inputAtt is a boolean that indicates if the attribute to be removed
 * is an input attribute (otherwise is an output attribute)
 * @param whichAtt is the position of the attribute to be deleted.
 */
 '''
def removeAttribute( self,attToDel,  inputAtt,  whichAtt):
    newSize=0;

    #Getting the vector
    index = 0;
    if (inputAtt==False):
        newSize = --self.__numOutputAttributes;
        index = 1;
    else:
        newSize = --self.__numInputAttributes;

    #The number of undefined attributes is increased.
    self.numUndefinedAttributes+=1;

    #It search the absolute position of the attribute to be
    #removed in the list of undefined attributes
    undefPosition = Attributes.searchUndefPosition(attToDel);

    #Reserving auxiliar memory to reconstruct the input or output
    nominalValuesAux  = str[newSize];
    intNominalValuesAux  = int[newSize];
    realValuesAux     = float[newSize];
    missingValuesAux = float[newSize];

    #Reserving auxiliar memory to reconstruct the undefined att's
    nominalValuesUndef    = str[self.numUndefinedAttributes];
    intNominalValuesUndef    = int[self.numUndefinedAttributes];
    realValuesUndef          = float[self.numUndefinedAttributes];
    missingValuesUndef      = float[self.numUndefinedAttributes];

    #Copying the values without the removed attribute
    k=0;
    self.anyMissingValue[index] = False;
    for i in range(0, newSize+1):
        if (i != whichAtt):
            nominalValuesAux[k] = self.nominalValues[index][i];
            intNominalValuesAux[k] = self.intNominalValues[index][i];
            realValuesAux[k] = self.realValues[index][i];
            missingValuesAux[k] = self.missingValues[index][i];
            if (missingValuesAux[k]) :
                self.anyMissingValue[index] = True;
            k+=1;

    else:
            nominalValuesUndef[undefPosition]       = self.nominalValues[index][i];
            intNominalValuesUndef[undefPosition]    = self.intNominalValues[index][i];
            realValuesUndef[undefPosition]          = self.realValues[index][i];
            missingValuesUndef[undefPosition]       = self.missingValues[index][i];



    #Copying the rest of the undefined values
    k=0;
    for i in range(0, self.numUndefinedAttributes):
        if (i==undefPosition) :
            continue;
        nominalValuesUndef[i]       = self.nominalValues[Instance.ATT_NONDEF][k];
        intNominalValuesUndef[i]    = self.intNominalValues[Instance.ATT_NONDEF][k];
        realValuesUndef[i]          = self.realValues[Instance.ATT_NONDEF][k];
        missingValuesUndef[i]       = self.missingValues[Instance.ATT_NONDEF][k];
        k+=1;


    #Copying the new vectors without the information of the removed attribute.
    self.nominalValues[index]    = nominalValuesAux;
    self.intNominalValues[index] = intNominalValuesAux;
    self.realValues[index]       = realValuesAux;
    self.missingValues[index]    = missingValuesAux;
    #The undefined attributes
    self.nominalValues[Instance.ATT_NONDEF] = nominalValuesUndef;
    self.intNominalValues[Instance.ATT_NONDEF] = intNominalValuesUndef;
    self.realValues[Instance.ATT_NONDEF] = realValuesUndef;
    self.missingValues[Instance.ATT_NONDEF] = missingValuesUndef;
#end removeAttribute

'''
/////////////////////////////////////////////////////////////////////////////
//	Other Instance functions                        //
/////////////////////////////////////////////////////////////////////////////

/**
 * It does return an string with the instance information. The format is the
 * same as the read one (keel format). Only are included in the string those
 * attributes that are defined as inputs or outputs. So, NON-SPECIFIED-DIRECTION
 * attributes are not included to this string.
 * The order followed is: first, all input attributes are writen, in the order
 * in which they have been read. After that, the output attributes are write.
 * This can alter the initial order, but never mind if the output writen
 * has the inputs and outputs correctly defined.
 * @return a String with the attribute information.
 */
 '''
def toStringFunction(self):
    aux = "";
    ending = ",";
    for i in range(0,self.numInputAttributes):
        if (i == self.numInputAttributes-1 and self.numOutputAttributes == 0) :
            ending = "";
        inputAttrType=Attributes.getInputAttribute(i).getType();
        if(inputAttrType== Attribute.NOMINAL):
            aux += self.nominalValues[0][i];

        if( inputAttrType==Attribute.INTEGER):
            aux += str(self.realValues[0][i]);

        if( inputAttrType==Attribute.REAL):
            aux += str(self.realValues[0][i]);


        aux += ending;

    ending = ",";
    for i in range(0,self.numOutputAttributes):
        if (i == self.numOutputAttributes-1) :
            ending = "";
        outputAttrType=Attributes.getOutputAttribute(i).getType();
        if(outputAttrType== Attribute.NOMINAL):
            aux += self.nominalValues[1][i];

        if(outputAttrType== Attribute.INTEGER):
            aux += str(self.realValues[1][i]);

        if(outputAttrType==Attribute.REAL):
            aux += str(self.realValues[1][i]);

        aux += ending;

    return aux;
#end toString

#	NEW FUNCTIONS DEFINED FOR NON-STATIC ATTRIBUTES

def printFunction ( self,instAttributes,  out):
    out.print("    > Inputs: ");
    for i in range(0, self.numInputAttributes):
        inputAttrType=instAttributes.getInputAttribute(i).getType();
        if (inputAttrType==Attribute.NOMINAL):
            out.print(self.nominalValues[Instance.ATT_INPUT][i]);

        if(inputAttrType== Attribute.INTEGER):
            out.print(self.realValues[Instance.ATT_INPUT][i]);

        if(inputAttrType== Attribute.REAL):
            out.print(self.realValues[Instance.ATT_INPUT][i]);

    out.print("\n    > Outputs: ");
    for i in range (0, self.numOutputAttributes):
        outputAttrType=self.__instAttributes.getOutputAttribute(i).getType();
        if(outputAttrType== Attribute.NOMINAL):
            out.print(self.nominalValues[Instance.ATT_OUTPUT][i]);

        if(outputAttrType== Attribute.INTEGER):
            out.print(self.realValues[Instance.ATT_OUTPUT][i]);

        if(outputAttrType== Attribute.REAL):
            out.print(self.realValues[Instance.ATT_OUTPUT][i]);

    out.print("\n    > Undefined: ");
    for  i in range(0,self.numUndefinedAttributes):
       outputAttrType=instAttributes.getOutputAttribute(i).getType();
       if (outputAttrType== Attribute.NOMINAL):
        out.print(self.nominalValues[Instance.ATT_OUTPUT][i]);
       elif(outputAttrType== Attribute.INTEGER):
        out.print(self.realValues[Instance.ATT_OUTPUT][i]);
       elif(outputAttrType == Attribute.REAL):
        out.print(self.realValues[Instance.ATT_OUTPUT][i]);
#end print
'''
 * It prints the instance to the specified PrintWriter.
 * The attribtes order is the same as the one in the
 * original file.
 * @param out is the PrintWriter where to print.
'''
def printAsOriginal ( instAttributes,  out):
    inCount = 0,
    outCount = 0,
    undefCount=0,
    count=0;
    numAttributes = instAttributes.getNumAttributes();
    for count in range(0, numAttributes):
        at = instAttributes.getAttribute(count);
        directionAttribute= at.getDirectionAttribute();
        if(directionAttribute== Attribute.INPUT):
            printAttribute(out, Instance.ATT_INPUT,   inCount, at.getType());
            inCount+=1;

        elif(directionAttribute==  Attribute.OUTPUT):
            printAttribute(out, Instance.ATT_OUTPUT, outCount, at.getType());
            outCount+=1;

        elif(directionAttribute== Attribute.DIR_NOT_DEF):
            printAttribute(out, Instance.ATT_NONDEF, undefCount, at.getType());
            undefCount+=1;


    if(count+1 <numAttributes) :
        out.print(",");

#end printAsOriginal


'''
 * It does print the instance information
'''
def print ( self,instAttributes ):
    print("  > Inputs ("+self.numInputAttributes+"): ");

    for i in range(0,self.numInputAttributes):
        if (self.missingValues[Instance.ATT_INPUT][i]):
            print("?");

        else:
            inputAttributeType= instAttributes.getInputAttribute(i).getType();
            if(inputAttributeType== Attribute.NOMINAL):
                print(self.nominalValues[Instance.ATT_INPUT][i]);

            elif(inputAttributeType== Attribute.INTEGER):
                print(self.realValues[Instance.ATT_INPUT][i]);

            else:
                if(inputAttributeType== Attribute.REAL):
                    print(self.realValues[Instance.ATT_INPUT][i]);



        print("  ");

    print("  > Outputs ("+self.numOutputAttributes+"): ");
    for i in range (0,self.numOutputAttributes):
        if (self.missingValues[Instance.ATT_OUTPUT][i]):
            print("?");

        else:
            outputAttrType=self.__instAttributes.getOutputAttribute(i).getType();
            if(outputAttrType==Attribute.NOMINAL):
                print(self.nominalValues[Instance.ATT_OUTPUT][i]);

            elif(outputAttrType== Attribute.INTEGER):
                print(self.realValues[Instance.ATT_OUTPUT][i]);

            elif(outputAttrType== Attribute.REAL):
                print(self.realValues[Instance.ATT_OUTPUT][i]);


    print("  ");


    print("  > Undefined ("+self.__numUndefinedAttributes+"): ");
    for i in range(0, self.__numUndefinedAttributes):
        if (self.__missingValues[Instance.ATT_NONDEF][i]):
            print("?");

        else:
            undefinedAttrType=self.__instAttributes.getUndefinedAttribute(i).getType();
            if(undefinedAttrType== Attribute.NOMINAL):
                print(self.nominalValues[Instance.ATT_NONDEF][i]);

            elif(undefinedAttrType== Attribute.INTEGER):
                print(self.realValues[Instance.ATT_NONDEF][i]);

            elif( undefinedAttrType== Attribute.REAL):
                print(self.realValues[Instance.ATT_NONDEF][i]);

        print("  ");

    #end print

'''
/**
 * Obtains the normalized input attributes from a InstanceAttribute definition
 * @param instAttributes The Attributes definition needed to normalize
 * @return A new allocated array with the input values normalized
 */
 
 '''
def getNormalizedInputValues(self,  instAttributes ):
    norm = float[self.realValues[0].length];
    for i in range(0, norm.length):
        if (self,missingValues[0][i]==False):
            norm[i] = instAttributes.getInputAttribute(i).normalizeValue(self.realValues[0][i]);
        else:
            norm[i] = -1.;

    return norm;
#end getNormalizedInputValues

'''
 * Obtains the normalized output attributes from a InstanceAttribute definition
 * @param instAttributes The Attributes definition needed to normalize
 * @return A new allocated array with the output values normalized
'''
def  getNormalizedOutputValues( self, instAttributes ):
    norm = float[self.realValues[1].length];
    for i in range(0, norm.length):
        if (self.missingValues[1][i]==False):
            norm[i] = instAttributes.getOutputAttribute(i).normalizeValue(realValues[1][i]);
        else:
            norm[i] = -1.;

    return norm;
#end getNormalizedOutputValues

'''
 * Set a new value of a given input attribute in this instance (integer or real)
 * @param instAttributes The Attributes reference definition
 * @param pos The position of the input attribute to be changed in instAttributes
 * @param value The new value
 * @return true if succeeded, false otherwise
'''
def setInputNumericValue( self,instAttributes,  pos,  value):
    at = Attribute(instAttributes.getInputAttribute(pos));
    if (at.getType() == Attribute.NOMINAL) :
        return False;
    else:
        if (at.isInBounds(value)):
            self.realValues[0][pos] = value;
            self.missingValues[0][pos] = False;
            self.anyMissingValue[0] = False;
            for i in range(0, self.missingValues[0].length):
                self.anyMissingValue[0] |= self.missingValues[0][i];

        else :
         return False;

    return True;
# end setInputNumericValue
'''
/**
 * Set a new value of a given output attribute in this instance (integer or real)
 * @param instAttributes The Attributes reference definition
 * @param pos The position of the output attribute to be changed in instAttributes
 * @param value The new value
 * @return true if succeeded, false otherwise
'''
def  setOutputNumericValue( self,instAttributes,  pos,  value):
    at = Attribute(self.__instAttributes.getOutputAttribute(pos));
    if (at.getType() == Attribute.NOMINAL) :
      return False;
    else:
        if (at.isInBounds(value)):
            self.realValues[1][pos] = value;
            self.missingValues[1][pos] = False;
            self.anyMissingValue[1] = False;
            for  i in range(0,self.missingValues[1].length):
                self.anyMissingValue[1] |= self.missingValues[1][i];

        else :
          return False;

    return True;
# end setInputNumericValue

'''
 * Set a new value of a given input attribute in this instance (nominal)
 * @param instAttributes The Attributes reference definition
 * @param pos The position of the input attribute to be changed in instAttributes
 * @param value The new value
 * @return true if succeeded, false otherwise
'''
def  setInputNominalValue( self,instAttributes,  pos,  value):
    at = Attribute(self.__instAttributes.getInputAttribute(pos));
    if (at.getType() != Attribute.NOMINAL) :
      return False;
    else:
        if (at.convertNominalValue(value) != -1):
            self.nominalValues[0][pos] = value;
            self.intNominalValues[0][pos] = at.convertNominalValue(value);
            self.realValues[0][pos] = self.intNominalValues[0][pos];
            self.missingValues[0][pos] = False;
            self.anyMissingValue[0] = False;
            for i in range (0, self.missingValues[0].length):
                self.anyMissingValue[0] |= self.missingValues[0][i];

        else :
         return False;

    return True;
#end setInputNominalValue

'''
 * Set a new value of a given output attribute in this instance (nominal)
 * @param instAttributes The Attributes reference definition
 * @param pos The position of the output attribute to be changed in instAttributes
 * @param value The new value
 * @return true if succeeded, false otherwise
'''
def setOutputNominalValue( self,instAttributes,  pos,  value):
    at = Attribute(self.__instAttributes.getOutputAttribute(pos));
    if (at.getType() != Attribute.NOMINAL) :
      return False;
    else:
        if (at.convertNominalValue(value) != -1):
            self.nominalValues[1][pos] = value;
            self.intNominalValues[1][pos] = at.convertNominalValue(value);
            self.realValues[1][pos] = self.intNominalValues[0][pos];
            self.missingValues[1][pos] = False;
            self.anyMissingValue[1] = False;
            for i in range (0, self.missingValues[1].length):
                self.anyMissingValue[1] |= self.missingValues[1][i];

        else :
          return False;

    return True;
#end setOutputNominalValue

def removeAttribute( self,instAttributes,  attToDel,  inputAtt,  whichAtt):
    newSize=0;

    #Getting the vector
    index = 0;
    if (inputAtt==False):
        newSize = --self.numOutputAttributes;
        index = 1;
    else :
        newSize = --self.numInputAttributes;

    #The number of undefined attributes is increased.
        self.numUndefinedAttributes+=1;

    #It search the absolute position of the attribute to be
    #removed in the list of undefined attributes
    undefPosition = instAttributes.searchUndefPosition(attToDel);

    #Reserving auxiliar memory to reconstruct the input or output
    nominalValuesAux  = str[newSize];
    intNominalValuesAux  = int[newSize];
    realValuesAux     = float[newSize];
    missingValuesAux = bool[newSize];

    #Reserving auxiliar memory to reconstruct the undefined att's
    nominalValuesUndef    = str[self.numUndefinedAttributes];
    intNominalValuesUndef    = int[self.numUndefinedAttributes];
    realValuesUndef          = float[self.numUndefinedAttributes];
    missingValuesUndef      = float[self.numUndefinedAttributes];

    #Copying the values without the removed attribute
    k=0;
    self.anyMissingValue[index] = False;
    for i in range(0, newSize+1):
        if (i != whichAtt):
            nominalValuesAux[k] = self.nominalValues[index][i];
            intNominalValuesAux[k] = self.intNominalValues[index][i];
            realValuesAux[k] = self.realValues[index][i];
            missingValuesAux[k] = self.missingValues[index][i];
            if (missingValuesAux[k]) :
                self.anyMissingValue[index] = True;
            k+=1;

    else:
            nominalValuesUndef[undefPosition]       = self.nominalValues[index][i];
            intNominalValuesUndef[undefPosition]    = self.intNominalValues[index][i];
            realValuesUndef[undefPosition]          = self.realValues[index][i];
            missingValuesUndef[undefPosition]       = self.missingValues[index][i];


    #Copying the rest of the undefined values
    k=0;
    for i in range(0, self.numUndefinedAttributes):
        if (i==undefPosition) :
            continue;

        nominalValuesUndef[i]       = self.nominalValues[Instance.ATT_NONDEF][k];
        intNominalValuesUndef[i]    = self.intNominalValues[Instance.ATT_NONDEF][k];
        realValuesUndef[i]          = self.realValues[Instance.ATT_NONDEF][k];
        missingValuesUndef[i]       = self.missingValues[Instance.ATT_NONDEF][k];
        k+=1;


    #Copying the new vectors without the information of the removed attribute.
    self.nominalValues[index]    = nominalValuesAux;
    self.intNominalValues[index] = intNominalValuesAux;
    self.realValues[index]       = realValuesAux;
    self.missingValues[index]    = missingValuesAux;
    #The undefined attributes
    self.nominalValues[Instance.ATT_NONDEF] = nominalValuesUndef;
    self.intNominalValues[Instance.ATT_NONDEF] = intNominalValuesUndef;
    self.realValues[Instance.ATT_NONDEF] = realValuesUndef;
    self.missingValues[Instance.ATT_NONDEF] = missingValuesUndef;
#end removeAttribute

'''
 * Prints the instance in KEEL format, according to the given Attributes definition
 * @param instAttributes The reference Attributes definition for printing
 * @return A new allocated String with the instance in KEEL format (CSV).
'''
def toString(self, instAttributes):
    aux = "";
    ending = ",";
    for i in range(0, self.numInputAttributes):
        if (i == self.numInputAttributes-1 and self.numOutputAttributes == 0):
            ending = "";
        instAttrType=instAttributes.getInputAttribute(i).getType();
        if(instAttrType== Attribute.NOMINAL):
            aux += self.nominalValues[0][i];

        if(instAttrType==  Attribute.INTEGER):
            aux += str(int(self.realValues[0][i]));

        if(instAttrType== Attribute.REAL):
            aux += str(float(self.realValues[0][i]));


    aux += ending;

    ending = ",";
    for i in range(0, self.numOutputAttributes):
        if (i == self.numOutputAttributes-1) :
            ending = "";
        instOutputAttrType=instAttributes.getOutputAttribute(i).getType();
        if(instOutputAttrType==Attribute.NOMINAL) :
          aux += self.nominalValues[1][i];

        elif(instOutputAttrType== Attribute.INTEGER):
            aux += str(self.realValues[1][i]);

        elif(instOutputAttrType==Attribute.REAL):
            aux += str(float(self.realValues[1][i]));
        aux += ending;

    return aux;
#end toString

#end of the class Instance






