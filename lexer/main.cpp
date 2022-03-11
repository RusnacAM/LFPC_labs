#include <iostream>
#include <fstream>
#include <cstdio>
using namespace std;

FILE * lfile = fopen("lexer.txt", "r");

enum Token{
    tok_eof = -1,

    tok_var = -2,
    tok_func = -3,
    tok_endfunc = -4,
    tok_for = -5,
    tok_next = -6,
    tok_if = -7,
    tok_else = -8,
    tok_endif = -9,

    //literals
    tok_identifier = -10,
    tok_int = -11,
    tok_float = -12,
    
    // arithmetic operators
    tok_assign = -13,
    tok_plus = -14,
    tok_minus = -15,
    tok_asterisk = -16,
    tok_slash = -17,
    tok_percent = -18,
    
    //relational operators
    tok_less = -19,
    tok_greater = -20,
    tok_lessequal = -21,
    tok_greaterequal = -22,
    tok_equal = -23,
    tok_notequal = -24,
    
    //logical operators
    tok_and = -25,
    tok_or = -26,
    
    // increment decrement operators
    tok_increment = -27,
    tok_decrement = -28,
    
    // demiliters
    tok_semicolon = -29,
    tok_comma = -30,
    
    tok_lparan = -31,
    tok_rparan = -32,
    tok_lsq = -33,
    tok_rsq = -34,
    
    tok_return = -35,
    tok_apostrophe = -36
};

static string IdentifierStr;
static double NumVal;
static string SymbolStr;

static int gettok(){
    static int LastChar = ' ';

    while(isspace(LastChar)){
        LastChar = getc(lfile);
    }

    if (isalpha(LastChar)){
        IdentifierStr = LastChar;
        while (isalnum((LastChar = getc(lfile)))){
            IdentifierStr += LastChar;
        }
        if(IdentifierStr == "var"){
            return tok_var;
        }
        if(IdentifierStr == "Function"){
            return tok_func;
        }
        if(IdentifierStr == "EndFunction"){
            return tok_endfunc;
        }
        if(IdentifierStr == "For"){
            return tok_for;
        }
        if(IdentifierStr == "Next"){
            return tok_next;
        }
        if(IdentifierStr == "If"){
            return tok_if;
        }
        if(IdentifierStr == "Else"){
            return tok_else;
        }
        if(IdentifierStr == "EndIf"){
            return tok_endif;
        }
        if(IdentifierStr == "return"){
            return tok_return;
        }

        return tok_identifier;
    }

    if(isdigit(LastChar) || LastChar == '.'){
        string NumStr;
        double number;
        bool integer = true;
        do {
            NumStr += LastChar;
            LastChar = getc(lfile);
            if(LastChar == '.') integer = false;
            
        } while (isdigit(LastChar) || LastChar == '.');

        number = strtod(NumStr.c_str(), nullptr);
        NumVal = number;

        if(integer){
            return tok_int;
        } else {
            return tok_float;
        }
    
    }
    
    if(ispunct(LastChar)){
        string symbol;
           do {
               symbol += LastChar;
               LastChar = getc(lfile);
                if(symbol == "(" || symbol == ")" || symbol == "[" || symbol == "]" || symbol == "++" || symbol == "--" || symbol == "'" || symbol == "\""){
                    break;
                }
            } while(ispunct(LastChar));
        
        SymbolStr = symbol;
        
            if(symbol == "="){
                return tok_assign;
            }
            if(symbol == "+"){
                return tok_plus;
            }
            if(symbol == ";"){
                return tok_semicolon;
            }
            if(symbol == "-"){
                return tok_minus;
            }
            if(symbol == "*"){
                return tok_asterisk;
            }
            if(symbol == "/"){
                return tok_slash;
            }
            if(symbol == "%"){
                return tok_percent;
            }
            if(symbol == "<"){
                return tok_less;
            }
            if(symbol == ">"){
                return tok_greater;
            }
            if(symbol == "<="){
                return tok_lessequal;
            }
            if(symbol == ">="){
                return tok_greaterequal;
            }
            if(symbol == "=="){
                return tok_equal;
            }
            if(symbol == "!="){
                return tok_notequal;
            }
            if(symbol == "&&"){
                return tok_and;
            }
            if(symbol == "||"){
                return tok_or;
            }
            if(symbol == "++"){
                return tok_increment;
            }
            if(symbol == "--"){
                return tok_decrement;
            }
            if(symbol == ","){
                return tok_comma;
            }
            if(symbol == "("){
                return tok_lparan;
            }
            if(symbol == ")"){
                return tok_rparan;
            }
            if(symbol == "["){
                return tok_lsq;
            }
            if(symbol == "]"){
                return tok_rsq;
            }
            if(symbol == "'" || symbol == "\""){
                return tok_apostrophe;
            }
    
        
        }

    if(LastChar == EOF){
        return tok_eof;
    }


    int ThisChar = LastChar;
    LastChar = getc(lfile);
    return ThisChar;
}

static int CurTok;
static int getNextToken(){
    if(CurTok == -1){
        cout<<"EOF"<<endl;
    }
    else if(CurTok == -2){
        cout<<"Literal "<<IdentifierStr<<" : "<<"VARIABLE"<<endl;
    }
    else if(CurTok == -3){
        cout<<"Literal "<<IdentifierStr<<" : "<<"FUNCTION"<<endl;
    }
    else if(CurTok == -4){
        cout<<"Literal "<<IdentifierStr<<" : "<<"ENDFUNCTION"<<endl;
    }
    else if(CurTok == -5){
        cout<<"Literal "<<IdentifierStr<<" : "<<"FOR"<<endl;
    }
    else if(CurTok == -6){
        cout<<"Literal "<<IdentifierStr<<" : "<<"NEXT"<<endl;
    }
    else if(CurTok == -7){
        cout<<"Literal "<<IdentifierStr<<" : "<<"IF"<<endl;
    }
    else if(CurTok == -8){
        cout<<"Literal "<<IdentifierStr<<" : "<<"ELSE"<<endl;
    }
    else if(CurTok == -9){
        cout<<"Literal "<<IdentifierStr<<" : "<<"ENDIF"<<endl;
    }
    else if(CurTok == -10){
        cout<<"Literal "<<IdentifierStr<<" : "<<"IDENTIFIER"<<endl;
    }
    else if(CurTok == -11){
        cout<<"Literal "<<NumVal<<" : "<<"INTEGER"<<endl;
    }
    else if(CurTok == -12){
        cout<<"Literal "<<NumVal<<" : "<<"FLOAT"<<endl;
    }
    else if(CurTok == -13){
        cout<<"Literal "<<SymbolStr<<" : "<<"ASSIGN"<<endl;
    }
    else if(CurTok == -14){
        cout<<"Literal "<<SymbolStr<<" : "<<"PLUS"<<endl;
    }
    else if(CurTok == -15){
        cout<<"Literal "<<SymbolStr<<" : "<<"MINUS"<<endl;
    }
    else if(CurTok == -16){
        cout<<"Literal "<<SymbolStr<<" : "<<"ASTERISK"<<endl;
    }
    else if(CurTok == -17){
        cout<<"Literal "<<SymbolStr<<" : "<<"SLASH"<<endl;
    }
    else if(CurTok == -18){
        cout<<"Literal "<<SymbolStr<<" : "<<"PERCENT"<<endl;
    }
    else if(CurTok == -19){
        cout<<"Literal "<<SymbolStr<<" : "<<"LESS"<<endl;
    }
    else if(CurTok == -20){
        cout<<"Literal "<<SymbolStr<<" : "<<"GREATER"<<endl;
    }
    else if(CurTok == -21){
        cout<<"Literal "<<SymbolStr<<" : "<<"LESSEQUAL"<<endl;
    }
    else if(CurTok == -22){
        cout<<"Literal "<<SymbolStr<<" : "<<"GREATEREQUAL"<<endl;
    }
    else if(CurTok == -23){
        cout<<"Literal "<<SymbolStr<<" : "<<"EQUAL"<<endl;
    }
    else if(CurTok == -24){
        cout<<"Literal "<<SymbolStr<<" : "<<"NOTEQUAL"<<endl;
    }
    else if(CurTok == -25){
        cout<<"Literal "<<SymbolStr<<" : "<<"AND"<<endl;
    }
    else if(CurTok == -26){
        cout<<"Literal "<<SymbolStr<<" : "<<"OR"<<endl;
    }
    else if(CurTok == -27){
        cout<<"Literal "<<SymbolStr<<" : "<<"INCREMENT"<<endl;
    }
    else if(CurTok == -28){
        cout<<"Literal "<<SymbolStr<<" : "<<"DECREMENT"<<endl;
    }
    else if(CurTok == -29){
        cout<<"Literal "<<SymbolStr<<" : "<<"SEMICOLON"<<endl;
    }
    else if(CurTok == -30){
        cout<<"Literal "<<SymbolStr<<" : "<<"COMMA"<<endl;
    }
    else if(CurTok == -31){
        cout<<"Literal "<<SymbolStr<<" : "<<"LEFTPARANTHESIS"<<endl;
    }
    else if(CurTok == -32){
        cout<<"Literal "<<SymbolStr<<" : "<<"RIGHTPARANTHESIS"<<endl;
    }
    else if(CurTok == -33){
        cout<<"Literal "<<SymbolStr<<" : "<<"LEFTSQUAREBRACKET"<<endl;
    }
    else if(CurTok == -34){
        cout<<"Literal "<<SymbolStr<<" : "<<"RIGHTSQUAREBRACKET"<<endl;
    }
    else if(CurTok == -35){
        cout<<"Literal "<<SymbolStr<<" : "<<"RETURN"<<endl;
    }
    else if(CurTok == -36){
        cout<<"Literal "<<SymbolStr<<" : "<<"APOSTROPHE"<<endl;
    }
     
    return CurTok = gettok();
}

static void MainLoop(){
    while (true){
        switch (CurTok){
        case tok_eof:
            return;
        default:
            getNextToken();
            break;
        }
    }
}

int main(){
    ifstream lfile;
    string lines;
    lfile.open("lexer.txt");
    cout<<"CODE:"<<endl;
        while(getline(lfile, lines)){
        cout<<lines<<endl;
    }
    cout<<endl<<endl;
    getNextToken();
    MainLoop();
}
