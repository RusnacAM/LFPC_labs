package lab2;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;

public class Conversion {
    static LinkedHashMap<String, LinkedHashMap<String, List<String>>> DFA = new LinkedHashMap<>();
    static ArrayList<String> intermedVals = new ArrayList<>();
    static ArrayList<String> vals = new ArrayList<>();
    static ArrayList<String> stateSet = new ArrayList<>();
    static ArrayList<String> allStates = new ArrayList<>();
    static ArrayList<String> newStates = new ArrayList<>();


    static void buildDFA (LinkedHashMap<String, LinkedHashMap<String, List<String>>> nfa, String start, String fin){

        getStatesVals(nfa);
        System.out.println("");
        // Steps NFA transition table
        buildTransNFA(nfa, start, fin);
        System.out.println("");
        // Conversion to DFA
        convFirstRow(nfa, start);
        convRows(nfa);
        // Steps DFA transition table
        buildTransDFA(start, fin);

        System.out.println("Converted DFA: ");
        for(String key: DFA.keySet()){
            System.out.println(key + " = " + DFA.get(key));
        }

    }

    static void getStatesVals(LinkedHashMap<String, LinkedHashMap<String, List<String>>> trNFA){
        for(String outerKey: trNFA.keySet()){
            LinkedHashMap<String, List<String>> innerMap = trNFA.get(outerKey);
            stateSet.add(outerKey);
            intermedVals.addAll(innerMap.keySet());
        }

        for(int i = 0; i < intermedVals.size(); i++){
            boolean flag = false;
            for(int j = 0; j < i; j++){
                if(intermedVals.get(i).equals(intermedVals.get(j))){
                    flag = true;
                    break;
                }
            } if(!flag){
                vals.add(intermedVals.get(i));
            }
        }
    }

    static void buildTransNFA (LinkedHashMap<String, LinkedHashMap<String, List<String>>> trNFA, String st, String f){
        int rowSize = vals.size() + 1;
        int colSize = stateSet.size();
        String[][] transNFA = new String[rowSize][colSize];

        System.out.println("NFA " + "  a " + "   b " + "   c ");
        System.out.println("-------------------");
        for(int i = 0; i < rowSize; i++){
            for(int j = 0; j < colSize; j++){
                if( j == 0) {
                    transNFA[i][j] = stateSet.get(i);
                    if(transNFA[i][j].equals(st)){
                        transNFA[i][j] = "->" + st;
                    } else if(transNFA[i][j].equals(f)){
                        transNFA[i][j] = "*" + f;
                    }
                }
            }
        }

        for(int i = 0; i < rowSize; i++){
            String currState = "q" + i;
            //System.out.println(currState);
            for(int j = 1; j < colSize; j++){
                if( j == 1){
                    if(!trNFA.get(currState).containsKey("a")){
                        transNFA[i][j] = "0";
                    } else {
                        transNFA[i][j] = String.valueOf(trNFA.get(currState).get("a"));
                    }
                } else if( j == 2){

                    if(!trNFA.get(currState).containsKey("b")){
                        transNFA[i][j] = "0";
                    } else {
                        transNFA[i][j] = String.valueOf(trNFA.get(currState).get("b"));
                    }
                } else if( j == 3){
                    if(!trNFA.get(currState).containsKey("c")){
                        transNFA[i][j] = "0";
                    } else {
                        transNFA[i][j] = String.valueOf(trNFA.get(currState).get("c"));
                    }
                }
            }
        }

        for(int i = 0; i < rowSize; i++){
            for(int j = 0; j < colSize; j++){
                System.out.print(transNFA[i][j] + " ");
            }
            System.out.println(" ");
        }
    }

    static void buildTransDFA(String st, String f){
        int rowSize = allStates.size();
        int colSize = vals.size() + 1;
        String[][] transDFA = new String[rowSize][colSize];

        System.out.println("DFA " + "  a " + "   b " + "   c ");
        System.out.println("-------------------");
        int count = 0;
        for(int i = 0; i < rowSize; i++){
            String currState = allStates.get(i);
            //System.out.println(currState);
            for(int j = 0; j < colSize; j++){
                if( j == 0) {
                    transDFA[i][j] = allStates.get(i);
                    if(transDFA[i][j].equals(st)){
                        transDFA[i][j] = "->" + st;
                    } else if(transDFA[i][j].equals(f)){
                        transDFA[i][j] = "*" + f;
                    }
                } else if( j == 1){
                    if(!DFA.get(currState).containsKey("a")){
                        transDFA[i][j] = "0";
                    } else {
                        transDFA[i][j] = String.valueOf(DFA.get(currState).get("a"));
                    }
                } else if( j == 2){
                    if(!DFA.get(currState).containsKey("b")){
                        transDFA[i][j] = "0";
                    } else {
                        transDFA[i][j] = String.valueOf(DFA.get(currState).get("b"));
                    }
                } else if( j == 3){
                    if(!DFA.get(currState).containsKey("c")){
                        transDFA[i][j] = "0";
                    } else {
                        transDFA[i][j] = String.valueOf(DFA.get(currState).get("c"));
                    }
                }
            }  count++;
            for(int k = 0; k < count; k++){
                for(int n = 0; n < colSize; n++){
                    System.out.print(transDFA[k][n] + " ");
                }
                System.out.println(" ");
            } System.out.println(" ");

        }
    }

    static void convFirstRow(LinkedHashMap<String, LinkedHashMap<String, List<String>>> trNFA, String st){
        for(String outerKey: trNFA.keySet()){
            LinkedHashMap<String, List<String>> innerMap = trNFA.get(outerKey);
            //System.out.println(innerMap);
            if(outerKey.equals(st)){
                for(String innerKey: innerMap.keySet()){
                    List<String> val = innerMap.get(innerKey);
                    String joinedStr = String.join("", val);
                    Data.buildTransition(DFA, outerKey, innerKey, joinedStr);
                    allStates.add(outerKey);
                    allStates.add(joinedStr);
                    newStates.add(joinedStr);
                }
            }
        }
    }

    static void convRows(LinkedHashMap<String, LinkedHashMap<String, List<String>>> trNFA){
        while(newStates.size() != 0){
            String tempSt = "";
            for(String ns: newStates){
                if(ns.length() > 2){
                    for(int i = 0; i < ns.length(); i += 2){
                        int temp = i + 2;
                        String tempState = ns.substring(i, temp);
                        LinkedHashMap<String, List<String>> innerMap = trNFA.get(tempState);
                        for(String innerKey: innerMap.keySet()){
                            List<String> val = innerMap.get(innerKey);
                            String joinedStr = String.join("", val);
                            if(!allStates.contains(joinedStr)){
                                allStates.add(joinedStr);
                            }
                            if(!newStates.contains(joinedStr)){
                                tempSt = joinedStr;
                            }
                            Data.buildTransition(DFA, ns, innerKey, joinedStr);
                        }
                    }
                } else if(ns.length() == 2){
                    String tempState = ns.substring(0, 2);
                    LinkedHashMap<String, List<String>> innerMap = trNFA.get(tempState);
                    for(String innerKey: innerMap.keySet()){
                        List<String> val = innerMap.get(innerKey);
                        String joinedStr = String.join("", val);
                        if(!allStates.contains(joinedStr)){
                            allStates.add(joinedStr);
                        }
                        if(!newStates.contains(joinedStr)){
                            tempSt = joinedStr;
                        }
                        Data.buildTransition(DFA, ns, innerKey, joinedStr);
                    }
                }
            }
            if(!newStates.contains(tempSt)){
                newStates.add(tempSt);
            }
            newStates.remove(0);
        }
    }


}
