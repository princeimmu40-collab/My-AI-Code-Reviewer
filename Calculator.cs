using System;

public class Calculator {
    
    // బగ్ 1: రిటర్న్ టైప్ int. ఒకవేళ 5/2 చేస్తే 2.5 రావాలి, కానీ ఇది కేవలం 2 మాత్రమే ఇస్తుంది.
    public int Divide(int a, int b) {
        // బగ్ 2: జీరో డివిజన్ చెక్ లేదు (ప్రోగ్రామ్ క్రాష్ అవుతుంది)
        return a / b;
    }

    // బగ్ 3: సంఖ్యలు పెద్దవి అయితే (Overflow) హ్యాండిల్ చేయడం లేదు
    public int Add(int a, int b) {
        return a + b;
    }
    
    // బగ్ 4: లాగింగ్ ఏమీ లేదు, ఏదైనా ఎర్రర్ వస్తే డీబగ్ చేయడం కష్టం
    public void Calculate() {
        int result = Divide(10, 0); // ఇది కచ్చితంగా క్రాష్ అవుతుంది
    }
}
