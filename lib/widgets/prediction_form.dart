import 'package:flutter/material.dart';

class PredictionForm extends StatefulWidget {
  final Function(double) onPredict;
  const PredictionForm({super.key, required this.onPredict});

  @override
  State<PredictionForm> createState() => _PredictionFormState();
}

class _PredictionFormState extends State<PredictionForm> {
  final _formKey = GlobalKey<FormState>();
  final openCtrl = TextEditingController();
  final highCtrl = TextEditingController();
  final lowCtrl = TextEditingController();
  final volumeCtrl = TextEditingController();

  @override
  void dispose() {
    openCtrl.dispose();
    highCtrl.dispose();
    lowCtrl.dispose();
    volumeCtrl.dispose();
    super.dispose();
  }

  void _predict() {
    if (_formKey.currentState!.validate()) {
      // 🚀 sementara prediksi dummy
      double open = double.parse(openCtrl.text);
      double high = double.parse(highCtrl.text);
      double low = double.parse(lowCtrl.text);
      double volume = double.parse(volumeCtrl.text);

      double predicted = (open + high + low) / 3 + (volume * 0.00001);
      widget.onPredict(predicted);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          TextFormField(
            controller: openCtrl,
            decoration: const InputDecoration(labelText: "Open Price"),
            keyboardType: TextInputType.number,
            validator: (v) => v!.isEmpty ? "Masukkan nilai" : null,
          ),
          TextFormField(
            controller: highCtrl,
            decoration: const InputDecoration(labelText: "High Price"),
            keyboardType: TextInputType.number,
            validator: (v) => v!.isEmpty ? "Masukkan nilai" : null,
          ),
          TextFormField(
            controller: lowCtrl,
            decoration: const InputDecoration(labelText: "Low Price"),
            keyboardType: TextInputType.number,
            validator: (v) => v!.isEmpty ? "Masukkan nilai" : null,
          ),
          TextFormField(
            controller: volumeCtrl,
            decoration: const InputDecoration(labelText: "Volume"),
            keyboardType: TextInputType.number,
            validator: (v) => v!.isEmpty ? "Masukkan nilai" : null,
          ),
          const SizedBox(height: 15),
          ElevatedButton(
            onPressed: _predict,
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 12),
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8)),
            ),
            child: const Text("Prediksi"),
          )
        ],
      ),
    );
  }
}
