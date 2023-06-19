import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'api_interface.dart';
import 'utils.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key, required this.title});

  final String title;
  final selectedColor = const Color.fromRGBO(249, 181, 12, 1);
  final unSelectedColor = const Color.fromRGBO(88, 47, 195, 1);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    API().verify();
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: appbarComponent(title: widget.title),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(15, 40, 5, 0),
          child: Stack(
            alignment: Alignment.center,
            children: <Widget>[
              Container(
                margin: const EdgeInsets.fromLTRB(205, 25, 0, 0),
                child: SvgPicture.asset(
                  'assets/images/path.svg',
                  height: 115,
                ),
              ),
              const Text(
                'Step into Serenity: Discover, Rate, and Share Inspiring Walking Routes',
                style: TextStyle(
                    fontSize: 26, color: Color.fromRGBO(49, 65, 80, 1)),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: buildNavbar(
        selectedColor: widget.selectedColor,
        unSelectedColor: widget.unSelectedColor,
        currentPageIndex: 0,
        routes: ['/', '/discover', '/map', '/authenticate', '/profile'],
        context: context,
      ),
    );
  }
}
