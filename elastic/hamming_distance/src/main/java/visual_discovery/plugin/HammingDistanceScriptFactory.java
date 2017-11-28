package visual_discovery.plugin;

import org.elasticsearch.common.Nullable;
import org.elasticsearch.script.ExecutableScript;
import org.elasticsearch.script.NativeScriptFactory;

import java.util.Map;

public class HammingDistanceScriptFactory implements NativeScriptFactory {

    public ExecutableScript newScript(@Nullable Map<String, Object> params) {
        return new HammingDistanceScript(params);
    }

    public String getName() {
		return "hamming_distance";
	}

    @Override
    public boolean needsScores() {
        return false;
    }
}