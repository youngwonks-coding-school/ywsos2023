import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'api_interface.dart';
import 'utils.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key, required this.title});

  final String title;

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
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

    return Scaffold(
      appBar: appbarComponent(title: widget.title),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(15, 10, 15, 0),
          child: SingleChildScrollView(
            child: Column(
              children: [
                const Text(
                  'Wasting None, Feeding Everyone!',
                  style: TextStyle(fontSize: 31),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 5),
                const Text(
                  'Restaurants and Food Banks United',
                  style: TextStyle(
                    fontSize: 25,
                  ),
                  textAlign: TextAlign.center,
                ),
                const Text(
                  'Yum Union bridges the gap between restaurants with surplus food and food banks seeking donations. Join this revolutionary platform to reduce waste and hunger together!',
                  style: TextStyle(
                    fontSize: 15,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 15),
                const Text(
                  'FAQs',
                  style: TextStyle(
                    fontSize: 25,
                  ),
                  textAlign: TextAlign.center,
                ),
                const Text(
                  'How Can I Join?',
                  style: TextStyle(
                    fontSize: 20,
                    color: Color.fromRGBO(250, 200, 70, 1),
                  ),
                  textAlign: TextAlign.center,
                ),
                const Text(
                  'Simply Sign Up and provide the details of your restaurant or food bank.',
                  textAlign: TextAlign.center,
                ),
                const Text(
                  'Is it Free?',
                  style: TextStyle(
                    fontSize: 20,
                    color: Color.fromRGBO(250, 200, 70, 1),
                  ),
                  textAlign: TextAlign.center,
                ),
                const Text(
                  'Absolutely! Food Connect is free for both restaurants and food banks.',
                  textAlign: TextAlign.center,
                ),
                const Text(
                  'How Can I Contribute?',
                  style: TextStyle(
                    fontSize: 20,
                    color: Color.fromRGBO(250, 200, 70, 1),
                  ),
                  textAlign: TextAlign.center,
                ),
                RichText(
                  textAlign: TextAlign.center,
                  text: TextSpan(
                    style: const TextStyle(fontFamily: 'Nexa'),
                    children: [
                      const TextSpan(
                        text:
                            'We are an open source project. You can contribute through our ',
                        style: TextStyle(color: Colors.black),
                      ),
                      TextSpan(
                        text: 'Github',
                        style: const TextStyle(
                          color: Colors.blue,
                          decoration: TextDecoration.underline,
                        ),
                        recognizer: TapGestureRecognizer()
                          ..onTap = () {
                            launchUrl(Uri.parse(
                                'https://github.com/youngwonks-coding-school/ywsos2023'));
                          },
                      ),
                      const TextSpan(
                        text: '.',
                        style: TextStyle(color: Colors.black),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
      bottomNavigationBar: buildNavbar(
        currentPageIndex: 0,
        context: context,
      ),
    );
  }
}
