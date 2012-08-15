#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections
import sys

__author__ = "Krzysztof Wróbel"

class SimpleRBES:
  """
  SimpleRBES (Rule-Based Expert System) is one level rule system with rules in format:
    IF symptom [AND symptom] THEN hypothesis
  Additionally have abbility to learn confidential factors (CF) of rules.
  """
  
  def readStructure(self, path):
    """Reads rules from file with format: each line represents one rule, elements are splitted by comma and the last one is hypothesis.
    
    Args:
      path - path to file with test cases
    """
    f = open(path)
    self.structure = []
    for line in f:
      s = line.strip().split(',')
      h = s[-1]
      a = frozenset(s[0:-1])
      self.structure.append([a,h,None])
    f.close()
  
  def learnCF(self, path):
    """Reads test cases from file with format: each line represents one rule, elements are splitted by comma and the last one is hypothesis. Then learns confidential factors of rules.
    
    Args:
      path - path to file with test cases
    """
    f = open(path)
    db = []
    db_rules = set()
    for line in f:
      s = line.strip().split(',')
      h = s[-1]
      a = frozenset(s[0:-1])
      db.append((a,h))
      db_rules.add(a)
    f.close()
      
    if len(db_rules) != len(set(db)):
      print 'not consistent'
    
    self.__learn(db)
  
  def __learn(self, db):
    for record in self.structure:
      a = record[0]
      h = record[1]
      true = 0
      false = 0
      for a2,h2 in db:
	if a<=a2: #rule works
	  if h==h2:
	    true += 1
	  else:
	    false += 1
      if true+false>0:
	record[2] = float(true)/(true+false)
      else:
	record[2] = 0.0
      #print record
  
  def diagnose(self, symptomy):
    """Returns dictionary of diagnosed hipothesis with CF.
    
    Args:
      symptomy - A set of symptoms
    """
    hipotezy = collections.defaultdict(float)

    for record in self.structure:
      a = record[0]
      if a<=symptomy:
	h = record[1]
	cf = record[2]
	hipotezy[h] = max(hipotezy[h], cf)
    return hipotezy
    
  def diagnoseCF(self, symptomyCF):
    """Returns dictionary of diagnosed hipothesis with CF.
    
    Args:
      symptomyCF - A dictionary of symptoms witf CF.
    """
    symptomy=frozenset(symptomyCF.keys())
    hipotezy = collections.defaultdict(float)

    for record in self.structure:
      a = record[0]
      if a<=symptomy:
	h = record[1]
	cf = record[2]
	mini = 1.0
	for au in a:
	  mini = min(mini, symptomyCF[au])
	hipotezy[h] = max(hipotezy[h], cf*mini)
    return hipotezy
  
  def printRules(self):
    """Prints rules woth CF."""
    for record in self.structure:
      a = record[0]
      h = record[1]
      cf = record[2]
      print ', '.join(list(a)) + ' -> ' + h + ' (' + str(cf) + ')'

  def printDiagnoseCF(self, symptomyCF):
    """Prints sorted hypothesis for symptoms with CF.
    
    Args:
      symptomyCF - A dictionary of symptoms witf CF.
    """
    for h,cf in  sorted(self.diagnoseCF(symptomyCF).items(), key=lambda (k,v): (v,k), reverse=True):
      print h, cf
    
if __name__ == "__main__":
  srbes = SimpleRBES()
  srbes.readStructure(sys.argv[1])
  srbes.learnCF(sys.argv[1])
  srbes.printRules()

  print
  srbes.printDiagnoseCF({'AU15':0.8, 'AU17':0.9})
  print
  srbes.printDiagnoseCF({'AU9':1.0, 'AU10':1.0, 'AU27':0.3})
  print
  srbes.printDiagnoseCF({'AU12':1.0, 'AU6':0.8})
  print
  srbes.printDiagnoseCF({'AU4':0.9, 'AU10':1.0, 'AU9':0.2})
  print
  srbes.printDiagnoseCF({'AU1':0.9, 'AU5':0.8, 'AU20':0.6, 'AU25':0.4})
  print
  srbes.printDiagnoseCF({'AU27':0.9, 'AU26':0.9, 'AU5':0.9, 'AU1':0.7, 'AU2':0.7})