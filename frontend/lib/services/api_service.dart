import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class ApiService {
  // Ganti dengan URL Railway kamu
  static const String baseUrl = "https://YOUR-RAILWAY-URL.up.railway.app";

  static Future<Map<String, dynamic>?> fetchPrediction() async {
    try {
      final url = Uri.parse("$baseUrl/predict");
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data;
      } else {
        if (kDebugMode) {
          print("API Error: ${response.statusCode}");
        }
        return null;
      }
    } catch (e) {
      if (kDebugMode) {
        print("API Error: $e");
      }
      return null;
    }
  }
}
