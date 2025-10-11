import 'package:flutter/material.dart';
import '../services/api_service.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  Map<String, dynamic>? _predictionData;
  bool _isLoading = false;
  String? _error;

  Future<void> _getPrediction() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    final data = await ApiService.fetchPrediction();

    setState(() {
      _predictionData = data;
      _isLoading = false;
      if (data == null) {
        _error = "Gagal mendapatkan prediksi";
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A), // navy gelap
      appBar: AppBar(
        title: const Text("Prediksi Saham GGRM.JK"),
        backgroundColor: const Color(0xFF1E293B),
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Text(
              "Prediksi harga saham Gudang Garam (GGRM.JK) menggunakan AI",
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.white, fontSize: 16),
            ),
            const SizedBox(height: 30),

            ElevatedButton.icon(
              onPressed: _getPrediction,
              icon: const Icon(Icons.analytics),
              label: const Text("Dapatkan Prediksi"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.tealAccent[700],
                foregroundColor: Colors.white,
                minimumSize: const Size(double.infinity, 50),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),
            const SizedBox(height: 30),

            if (_isLoading)
              const CircularProgressIndicator(color: Colors.tealAccent),

            if (_error != null)
              Card(
                color: Colors.red[900],
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Text(
                    _error!,
                    style: const TextStyle(color: Colors.white),
                  ),
                ),
              ),

            if (_predictionData != null && !_isLoading)
              Card(
                color: const Color(0xFF1E293B),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                elevation: 6,
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    children: [
                      Text(
                        "Hasil Prediksi ${_predictionData!['ticker']}",
                        style: TextStyle(
                          color: Colors.tealAccent[400],
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 12),
                      Text(
                        "Rp ${_predictionData!['predicted_price'].toStringAsFixed(2)}",
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 32,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        "Tanggal: ${_predictionData!['date']}",
                        style: const TextStyle(color: Colors.grey, fontSize: 14),
                      ),
                    ],
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
