import 'package:flutter/material.dart';
import 'package:mobile/charts.dart';
import 'package:mobile/posts.dart';
import 'home_page.dart';
import 'authenticate.dart';
import 'profile.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Walk Wise',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
            seedColor: const Color.fromRGBO(187, 170, 159, 1)),
        useMaterial3: true,
        fontFamily: 'Nexa',
      ),
      initialRoute: '/',
      routes: {
        '/': ((context) => const HomePage(title: 'Walk Wise')),
        '/discover': ((context) => const HomePage(title: 'Discover Trails')),
        '/posts': ((context) => const Posts(title: 'Posts')),
        '/charts': (context) => const Charts(title: 'Posting Trends'),
        '/authenticate': (context) => const Authenticate(title: 'Authenticate'),
        '/profile': (context) => const Profile(title: 'Profile'),
      },
    );
  }
}
