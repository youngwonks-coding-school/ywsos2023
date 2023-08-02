import 'dart:math';
import 'package:intl/intl.dart';
import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'api_interface.dart';
import 'utils.dart';

class Charts extends StatefulWidget {
  const Charts({super.key, required this.title});

  final String title;
  final selectedColor = const Color.fromRGBO(249, 181, 12, 1);
  final unSelectedColor = const Color.fromRGBO(88, 47, 195, 1);

  @override
  State<Charts> createState() => _ChartsState();
}

class _ChartsState extends State<Charts> {
  bool loadingPosts = true;
  List<dynamic> posts = [];
  List<int> postsPerDayInLastWeek = [];
  List<int> postsPerMonthInLastHalfYear = [];
  List<int> data = [];
  List<String> aggregationOptions = ["Daily", "Monthly"];
  String dropdownValue = "Daily";

  String dailyChartLabel(double value) {
    DateTime now = DateTime.now();
    switch (value.toInt()) {
      case 0:
        return DateFormat.Md().format(now.subtract(const Duration(days: 6)));
      case 2:
        return DateFormat.Md().format(now.subtract(const Duration(days: 5)));
      case 4:
        return DateFormat.Md().format(now.subtract(const Duration(days: 4)));
      case 6:
        return DateFormat.Md().format(now.subtract(const Duration(days: 3)));
      case 8:
        return DateFormat.Md().format(now.subtract(const Duration(days: 2)));
      case 10:
        return DateFormat.Md().format(now.subtract(const Duration(days: 1)));
      case 12:
        return DateFormat.Md().format(now);
      default:
        return '';
    }
  }

  String monthlyChartLabel(double value) {
    DateTime now = DateTime.now();
    switch (value.toInt()) {
      case 0:
        return DateFormat("MMM").format(DateTime(0, now.month - 5));
      case 2:
        return DateFormat("MMM").format(DateTime(0, now.month - 4));
      case 4:
        return DateFormat("MMM").format(DateTime(0, now.month - 3));
      case 6:
        return DateFormat("MMM").format(DateTime(0, now.month - 2));
      case 8:
        return DateFormat("MMM").format(DateTime(0, now.month - 1));
      case 10:
        return DateFormat("MMM").format(now);
      default:
        return '';
    }
  }

  Widget bottomTitleWidgets(double value, TitleMeta meta) {
    const style = TextStyle(
      fontWeight: FontWeight.bold,
      fontSize: 15,
      height: 1.1,
    );
    Widget text;
    if (dropdownValue == "Daily") {
      text = Text(dailyChartLabel(value), style: style);
    } else if (dropdownValue == "Monthly") {
      text = Text(monthlyChartLabel(value), style: style);
    } else {
      text = const Text('');
    }

    return SideTitleWidget(
      axisSide: meta.axisSide,
      child: text,
    );
  }

  void getPostsPerDayInLastWeek() {
    List<int> postsPerDay = [0, 0, 0, 0, 0, 0, 0];

    for (final post in posts) {
      int daysAgo = daysBetween(post["time"], DateTime.now());
      if (daysAgo < 7) {
        postsPerDay[6 - daysAgo] += 1;
      }
    }

    postsPerDayInLastWeek = postsPerDay;
  }

  void getPostsPerMonthInLastHalfYear() {
    List<int> postsPerMonth = [0, 0, 0, 0, 0, 0];

    for (final post in posts) {
      int monthsAgo = monthsBetween(post["time"], DateTime.now());
      if (monthsAgo < 6) {
        postsPerMonth[5 - monthsAgo] += 1;
      }
    }

    postsPerMonthInLastHalfYear = postsPerMonth;
  }

  int daysBetween(DateTime from, DateTime to) {
    from = DateTime(from.year, from.month, from.day);
    to = DateTime(to.year, to.month, to.day);
    return (to.difference(from).inHours / 24).round();
  }

  int monthsBetween(DateTime from, DateTime to) {
    from = DateTime(from.year, from.month, from.day);
    to = DateTime(to.year, to.month, to.day);
    return (to.difference(from).inDays / 30).round();
  }

  void getData() async {
    loadingPosts = true;

    List<dynamic> postsData = (await API().getRestaurantPosts()).data;

    for (final post in postsData) {
      post["time"] =
          DateTime.fromMillisecondsSinceEpoch(int.parse(post["time"]) * 1000);
    }

    posts = postsData;

    setState(() {
      loadingPosts = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    API().verify().then((value) {
      if (value is Map) {
        if (value.containsKey('error')) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(value["error"]),
            ),
          );
        } else {
          setState(() {});
        }
      }
    });

    if (loadingPosts == true) {
      getData();
    } else {
      getPostsPerDayInLastWeek();
      getPostsPerMonthInLastHalfYear();
    }

    if (dropdownValue == "Daily") {
      data = postsPerDayInLastWeek;
    } else {
      data = postsPerMonthInLastHalfYear;
    }

    return Scaffold(
      appBar: appbarComponent(title: widget.title, backButton: true),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(5, 15, 5, 35),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              DropdownButton<String>(
                value: dropdownValue,
                icon: const Icon(Icons.arrow_downward),
                elevation: 16,
                style: const TextStyle(
                    color: Color.fromRGBO(50, 110, 180, 1), fontFamily: "Nexa"),
                underline: Container(
                  height: 2,
                  color: const Color.fromRGBO(50, 110, 180, 1),
                ),
                onChanged: (String? value) {
                  setState(() {
                    dropdownValue = value!;
                  });
                },
                items: aggregationOptions
                    .map<DropdownMenuItem<String>>((String value) {
                  return DropdownMenuItem<String>(
                    value: value,
                    child: Text(value),
                  );
                }).toList(),
              ),
              loadingPosts
                  ? const CircularProgressIndicator(
                      color: Color.fromRGBO(100, 125, 155, 1),
                      strokeWidth: 3,
                    )
                  : Expanded(
                      child: Padding(
                        padding: const EdgeInsets.only(right: 40),
                        child: LineChart(
                          LineChartData(
                            maxY: data.reduce(max).toDouble() + 1,
                            lineBarsData: [
                              LineChartBarData(
                                spots: [
                                  for (int i = 0; i < data.length; i++)
                                    FlSpot(
                                      i * 2,
                                      data[i].toDouble(),
                                    ),
                                ],
                                color: widget.unSelectedColor,
                                isCurved: true,
                                curveSmoothness: 0.2,
                                preventCurveOverShooting: true,
                              ),
                            ],
                            titlesData: FlTitlesData(
                              bottomTitles: AxisTitles(
                                sideTitles: SideTitles(
                                  getTitlesWidget: bottomTitleWidgets,
                                  showTitles: true,
                                ),
                              ),
                              topTitles: const AxisTitles(
                                sideTitles: SideTitles(
                                  showTitles: false,
                                ),
                              ),
                              rightTitles: const AxisTitles(
                                sideTitles: SideTitles(
                                  showTitles: false,
                                ),
                              ),
                            ),
                          ),
                          duration:
                              const Duration(milliseconds: 150),
                          curve: Curves.linear,
                        ),
                      ),
                    ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: buildNavbar(
        currentPageIndex: -1,
        context: context,
      ),
    );
  }
}
