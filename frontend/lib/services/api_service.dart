import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "https://stock-backend.up.railway.app";

  static Future<double?> fetchStockPrice(String symbol) async {
    try {
      final url = Uri.parse("$baseUrl/predict?symbol=$symbol");
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        if (data['price'] != null) {
          return (data['price'] as num).toDouble();
        }
      }

      return null;
    } catch (e) {
      if (kDebugMode) {
        print("API Error: $e");
      }
      return null;
    }
  }
}
