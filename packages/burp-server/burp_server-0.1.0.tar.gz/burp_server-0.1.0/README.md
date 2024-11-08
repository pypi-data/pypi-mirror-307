Annotated burp interfaces for python/jython

# Installation
    pip2 install burp_server
    
# Usage 1

    # Burp need to load each class explicitly
    from burp import IBurpExtender, IScannerCheck

    # This allow us to get typing hints for all burp classes in our IDE
    from burp import *

    class BurpExtender(IBurpExtender, IScannerCheck):
        def registerExtenderCallbacks(self, callbacks):  # type: (IBurpExtenderCallbacks) -> ()
            print "Loading plugin"
            callbacks.registerScannerCheck(self)
    
        def doPassiveScan(self, baseRequestResponse):  # type: (IHttpRequestResponse) -> List[IScanIssue]
            return []
    
        def doActiveScan(self, baseRequestResponse, insertionPoint):  # type: (IHttpRequestResponse, IScannerInsertionPoint) -> List[IScanIssue]
            return []
    

# Install Requires

    python>=3.6.0



    