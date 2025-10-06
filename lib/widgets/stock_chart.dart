import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class StockChart extends StatelessWidget {
  final List<FlSpot> data;

  const StockChart({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    if (data.isNotEmpty) {
      return LineChart(
        LineChartData(
          titlesData: const FlTitlesData(
            leftTitles: AxisTitles(
              sideTitles: SideTitles(showTitles: true, reservedSize: 44),
            ),
            bottomTitles: AxisTitles(
              sideTitles: SideTitles(showTitles: true, reservedSize: 30),
            ),
            rightTitles: AxisTitles(
              sideTitles: SideTitles(showTitles: false),
            ),
            topTitles: AxisTitles(
              sideTitles: SideTitles(showTitles: false),
            ),
          ),
          lineBarsData: [
            LineChartBarData(
              spots: data,
              isCurved: true,
              barWidth: 2,
              color: Colors.blue,
              belowBarData: BarAreaData(show: false),
            )
          ],
        ),
      );
    }

    // ✅ fallback kalau data kosong
    return const Center(
      child: Text(
        "Tidak ada data untuk ditampilkan",
        style: TextStyle(fontSize: 16, color: Colors.grey),
      ),
    );
  }
}
