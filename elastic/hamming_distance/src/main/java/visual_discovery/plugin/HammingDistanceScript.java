package visual_discovery.plugin;

import org.elasticsearch.index.fielddata.ScriptDocValues;
import org.elasticsearch.script.AbstractDoubleSearchScript;

import java.util.Map;
import java.util.List;

public class HammingDistanceScript extends AbstractDoubleSearchScript {

    private String field;
    private long[] hash;

    public HammingDistanceScript(String field, long[] hash) {
        this.field = field;
		this.hash = hash;
    }

    private double hammingDistance(long[] lhs, long[] rhs) {
        double distance = 0.0f;
        long v1, v2;
		for (int i = 0; i < lhs.length; i++) {
			v1 = lhs[i];
			v2 = rhs[i];

			distance += (32 - Long.bitCount(v1 ^ v2));
		}
//        distance += (32 - Long.bitCount(v1 ^ v2));

//        for (int i = 0, l = lhs.length(); i < l; i++) {
//            if (lhs.charAt(i) != rhs.charAt(i)) {
//                distance--;
//            }
//        }

        return distance;
    }

    @Override
    public double runAsDouble() {
        String str = ((ScriptDocValues.Strings) doc().get(field)).getValue();
        String[] array = str.split(",");  //Split the previous String for separate by commas
        System.out.println(str);
        long[] field_value = new long[array.length];
        for (int i = 0; i < array.length; i++)
            field_value[i] = Long.parseLong(array[i]);

        if (hash == null || field_value == null || hash.length != field_value.length) {
            return -1f;
        }

        return hammingDistance(field_value, hash);
    }
}