package visual_discovery.plugin;

import org.elasticsearch.common.Nullable;
import org.elasticsearch.script.ExecutableScript;
import org.elasticsearch.script.NativeScriptFactory;
import org.elasticsearch.script.ScriptException;

import java.util.Map;
import java.util.ArrayList;

public class HammingDistanceScriptFactory implements NativeScriptFactory {

    public ExecutableScript newScript(@Nullable Map<String, Object> params) {
        String field = (java.lang.String) params.get("field");
		if (field == null) {
			throw new ScriptException("Field data param field is missing", null, null, "hamming_distance", "native");
		}
		ArrayList<Number> hash_array = (ArrayList<Number>) params.get("hash");
		if (hash_array == null)
			throw new ScriptException("Param hash is missing", null, null, "hamming_distance", "native");
		long[] hash = new long[hash_array.size()];
		for (int i = 0; i < hash_array.size(); i++)
			hash[i] = hash_array.get(i).longValue();

        return new HammingDistanceScript(field, hash);
    }

    public String getName() {
		return "hamming_distance";
	}

    @Override
    public boolean needsScores() {
        return false;
    }
}