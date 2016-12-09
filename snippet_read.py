#!/usr/bin/env python3
"""snippet_ready.py: Read Snippet in XML form
"""
__author__ = 'colin@doch.org.uk'

# Require xml and argparse
import sys
import argparse
from xml.dom.minidom import parse, Node
from snippet import Snippet
from snippet import Token_type

def remove_blanks(node):
    for x in node.childNodes:
        if x.nodeType == Node.TEXT_NODE:
            if x.nodeValue:
                # Cleanout any empty lines
                x.nodeValue = x.nodeValue.strip()
                x.nodeValue = x.nodeValue.rstrip('\n')
                if '' == x.nodeValue:
                    node.removeChild(x)
                    print("REMOVE")
        elif x.nodeType == Node.ELEMENT_NODE:
            remove_blanks(x)

def handleSnippetsXML(dom):
    slist = []

    snippets = dom.getElementsByTagName('snippet')
    for snippet in snippets:
        slist.append(handleSnippetTag(dom, snippet, False, False))
        print(slist)

def handleSnippetTag(dom, snippet, nochild, childtextonly):
    slist = []

    if nochild:
        print("Error: Child Node where one should not exist")
        return slist

    for child in snippet.childNodes:

        #remove_blanks(child)

        # Do not continue if NODE type is not what is expected!
        if child.nodeType != Node.TEXT_NODE and childtextonly:
            print("Error: Only a Child NODE == TEXT_NODE expected!")
            return slist

        if child.nodeType == Node.TEXT_NODE:
            ndict = {}
            ndict['type'] = Token_type.text
            ndict['value'] = child.nodeValue
            print(ndict)
            slist.append(ndict)

            # A TEXT_NODE is always a leaf
            return slist

        if child.nodeType == Node.ELEMENT_NODE:
            ndict = {}
            if child.tagName == 'token':
                ndict['type'] = Token_type.token
                nochild = False
                childtextonly = True
                ndict['value'] = 'this_is_a_test'
            elif child.tagName == 'list':
                ndict['type'] = Token_type.list_start
                ndict['value'] = '{'
                nochild = False
                childtextonly = False
            elif child.tagName == 'newline':
                ndict['type'] = Token_type.newline
                ndict['value'] = '\n'
                nochild = True
                childtextonly = True
            elif child.tagName == 'text':
                ndict['type' ] = Token_type.text
                nochild = False
                childtextonly = True
            else:
                print("Error! Unknown tagName : %s" % child.tagName)

            print(ndict)

            # Don't process children if not permitted
            if child.hasChildNodes and nochild:
                print("Error! Child Node, where a child Node is not expected")
                return ndict

            # Process children of this Node if they exist
            if child.hasChildNodes:
                #remove_blanks(child)

                child_slist = handleSnippetTag(dom, child,\
                                               nochild, childtextonly)

                if child.tagName == 'list':
                    slist.append(ndict)
                    ndict = {}
                    ndict['type'] = Token_type.list_end
                    ndict['value'] = '}'
                    slist.append(child_slist)
                    slist.append(ndict)
                    print(ndict)
                elif child.tagName == 'text':
                    child_ndict = {}
                    if child_slist == None:
                        child_ndict['value'] = ''
                    else:
                        child_ndict = child_slist[0]
                    ndict['value'] = child_ndict['value']
                    slist.append(ndict)
                    print(ndict)
                elif child.tagName == 'token':
                    ndict['value'] = thetext
                    slist.append(ndict)
                    print(ndict)
                else:
                    slist.append(ndict)

                return slist

            else:
                slist.append(ndict)
                return slist

def snippet_get(xml_file):
    if xml_file:
        dom = parse(xml_file)
        remove_blanks(dom)
        handleSnippetsXML(dom)
        return []
    else:
        exit(1)

def main():
    # Start by parsing and sanity checking all input.

    parser = argparse.ArgumentParser(description='Parse XML for snippet')
    parser.add_argument('--xml', '-f', dest='xml',
                        help="The XML file")

    args = parser.parse_args()
    xml = args.xml

    test_snippet = snippet_get(xml)

if __name__ == "__main__":
    main()
