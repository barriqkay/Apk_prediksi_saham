import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const StockPredictApp());
}

class StockPredictApp extends StatelessWidget {
  const StockPredictApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Prediksi Harga Saham',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        fontFamily: 'Roboto',
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController _symbolController = TextEditingController();
  bool _loading = false;
  String? _prediction;
  String? _error;

  Future<void> _fetchPrediction() async {
    final symbol = _symbolController.text.trim();
    if (symbol.isEmpty) {
      setState(() => _error = "Kode saham tidak boleh kosong");
      return;
    }

    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      // 🔗 GANTI URL INI DENGAN URL BACKEND RAILWAY KAMU
      final uri = Uri.parse(
          'https://YOUR-RAILWAY-URL.up.railway.app/predict?symbol=$symbol');
      final response = await http.get(uri);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          _prediction = data['prediction'].toString();
        });
      } else {
        setState(() => _error = 'Gagal memuat data (${response.statusCode})');
      }
    } catch (e) {
      setState(() => _error = 'Terjadi kesalahan: $e');
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.indigo,
        title: const Text(
          'Prediksi Harga Saham',
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: ListView(
          children: [
            const SizedBox(height: 20),
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(18),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black12,
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  )
                ],
              ),
              child: Column(
                children: [
                  const Text(
                    'Masukkan kode saham yang ingin kamu prediksi',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 16, color: Colors.black87),
                  ),
                  const SizedBox(height: 15),
                  TextField(
                    controller: _symbolController,
                    textCapitalization: TextCapitalization.characters,
                    decoration: InputDecoration(
                      labelText: 'Kode Saham (misal: AAPL)',
                      prefixIcon: const Icon(Icons.trending_up),
                      filled: true,
                      fillColor: Colors.grey[100],
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide.none,
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton.icon(
                    onPressed: _loading ? null : _fetchPrediction,
                    icon: const Icon(Icons.analytics),
                    label: const Text('Prediksi Sekarang'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.indigo,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      minimumSize: const Size(double.infinity, 50),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 40),
            if (_loading)
              const Center(
                child: CircularProgressIndicator(color: Colors.indigo),
              ),
            if (_error != null)
              Container(
                padding: const EdgeInsets.all(15),
                margin: const EdgeInsets.only(top: 10),
                decoration: BoxDecoration(
                  color: Colors.red[50],
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Text(
                  _error!,
                  style: const TextStyle(color: Colors.red, fontSize: 14),
                ),
              ),
            if (_prediction != null && !_loading)
              AnimatedContainer(
                duration: const Duration(milliseconds: 500),
                curve: Curves.easeOut,
                margin: const EdgeInsets.only(top: 20),
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Colors.indigo[50],
                  borderRadius: BorderRadius.circular(18),
                ),
                child: Column(
                  children: [
                    const Text(
                      '📈 Hasil Prediksi Harga Saham',
                      style:
                          TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 10),
                    Text(
                      _prediction!,
                      style: const TextStyle(
                        fontSize: 28,
                        color: Colors.indigo,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }
}

