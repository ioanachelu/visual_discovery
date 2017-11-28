package visual_discovery.plugin;

import java.util.ArrayList;
import java.util.List;

import org.elasticsearch.plugins.Plugin;
import org.elasticsearch.plugins.ScriptPlugin;
import org.elasticsearch.script.ScriptModule;
import org.elasticsearch.script.NativeScriptFactory;

import visual_discovery.plugin.HammingDistanceScriptFactory;

public class HammingDistancePlugin extends Plugin implements ScriptPlugin {

//    private static final String PLUGIN_NAME = "hamming_distance";
//
//    @Override
//    public String name() {
//        return PLUGIN_NAME;
//    }
//
//    @Override
//    public String description() {
//        return "A scoring function to calculate hamming distance between two hex encoded strings.";
//    }
//
//    public void onModule(ScriptModule scriptModule) {
//        scriptModule.registerScript(PLUGIN_NAME, HammingDistanceScriptFactory.class);
//    }
    public List<NativeScriptFactory> getNativeScripts() {
		List<NativeScriptFactory> list = new ArrayList<NativeScriptFactory>();
		list.add(new HammingDistanceScriptFactory());

		return list;
	}

}