import 'package:flutter/material.dart';

class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Settings")),
      body: ListView(
        children: const [
          ListTile(
            leading: Icon(Icons.info),
            title: Text("Tentang Aplikasi"),
            subtitle: Text("Versi 1.0 - Prediksi Saham"),
          ),
          ListTile(
            leading: Icon(Icons.person),
            title: Text("Pengembang"),
            subtitle: Text("Barriq Kaykaus Mujau"),
          ),
        ],
      ),
    );
  }
}
