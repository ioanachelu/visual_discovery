package visual_discovery.plugin;

import org.elasticsearch.index.fielddata.ScriptDocValues;
import org.elasticsearch.script.AbstractDoubleSearchScript;

import java.util.Map;

public class HammingDistanceScript extends AbstractDoubleSearchScript {

    private String field;
    private String hash;
    private int length;

    public HammingDistanceScript(Map<String, Object> params) {
        super();
        field = (String) params.get("field");
        hash = (String) params.get("hash");
        if (hash != null) {
            length = hash.length();
        }
    }

    private double hammingDistance(CharSequence lhs, CharSequence rhs) {
        double distance = (double) length;
        for (int i = 0, l = lhs.length(); i < l; i++) {
            if (lhs.charAt(i) != rhs.charAt(i)) {
                distance--;
            }
        }

        return distance;
    }

    @Override
    public double runAsDouble() {
        String fieldValue = ((ScriptDocValues.Strings) doc().get(field)).getValue();
        if (hash == null || fieldValue == null || fieldValue.length() != hash.length()) {
            return 0.0f;
        }

        return hammingDistance(fieldValue, hash);
    }
}