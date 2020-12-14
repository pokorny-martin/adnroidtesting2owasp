# androidtesting2owasp
Android_testing2OWASP is a tool for combining outputs of fully automatic frameworks/tools for android applications security testing.
Current supported frameworks are Androwarn, AndroPyTool (just Features_files output is currently supported), Androbugs and MobSF.
Outputs of each framework is parsed so only that parts relevant to testing scenarios defined in https://github.com/OWASP/owasp-masvs are covered. 
Combining of outputs is done with two rules in mind:  
1. boolean values - frameworks are not enough trustworthy, if one contradicts other in boolean valued property, the worst (for security score) is taken as result
2. any other (usually list of strings) - all data are taken, if any detailed information is supplied, none is deleted, all are taken; so the user has the most information to based his opinion on  

## Usage
```
python android_t2owasp.py -h
usage: android_t2owasp.py [-h] [-aw AW] [-ap AP] [-ab AB] [-sf SF] [-o O]

optional arguments:
  -h, --help  show this help message and exit
  -aw AW      Path to Androwarn output
  -ap AP      Path to AndroPyTool output
  -ab AB      Path to Androbugs output
  -sf SF      Path to MobSF output
  -o O        Path to output directory
 ```
  
Tested on python3.8.2.  
Uses just standard libraries.  
For older versions json and argparse might be required to install.  
