package spring.trading.domain;

import org.json.JSONArray;
import org.json.JSONObject;

public class OrderResult {
    private JSONObject result;
    private JSONArray resultArray;

    public JSONObject getResult() {
        return result;
    }

    public void setResult(JSONObject result) {
        this.result = result;
    }

    public JSONArray getResultArray() {
        return resultArray;
    }

    public void setResultArray(JSONArray resultArray) {
        this.resultArray = resultArray;
    }
}
