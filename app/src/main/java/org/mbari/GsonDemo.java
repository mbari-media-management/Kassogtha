package org.mbari;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import com.google.gson.GsonBuilder;
import org.mbari.vcr4j.sharktopoda.client.localization.Localization;

public class GsonDemo {

  public static void main(String[] args) throws Exception {
      var path = Paths.get(args[0]);
      var json = Files.readString(path, StandardCharsets.UTF_8);
      var gson = new GsonBuilder().create();
      var locs = gson.fromJson(json, Localization[].class);
  }
  
}
