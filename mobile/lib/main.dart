import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'home_page.dart';
import 'posts.dart';
import 'create_foodbank_post.dart';
import 'charts.dart';
import 'profile.dart';
import 'authenticate.dart';


final _router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomePage(title: 'Yum Union'),
    ),
    GoRoute(
      path: '/discover',
      builder: (context, state) => const HomePage(title: 'Discover'),
    ),
    GoRoute(
      path: '/posts',
      builder: (context, state) => const Posts(title: 'Posts'),
    ),
    GoRoute(
      path: '/charts',
      builder: (context, state) => const Charts(title: 'Charts'),
    ),
    GoRoute(
      path: '/authenticate',
      builder: (context, state) => const Authenticate(title: 'Authenticate'),
    ),
    GoRoute(
      path: '/profile',
      builder: (context, state) => const Profile(title: 'Profile'),
    ),
    GoRoute(
      path: '/create-foodbank-post',
      builder: (context, state) => const CreatePost(title: 'Create Post'),
    ),
  ],
);

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Yum Union',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
            seedColor: const Color.fromRGBO(187, 170, 159, 1)),
        useMaterial3: true,
        fontFamily: 'Nexa',
      ),
      routerConfig: _router,
    );
  }
}
