import 'package:flutter/material.dart';
import 'api_interface.dart';
import 'utils.dart';

class Posts extends StatefulWidget {
  const Posts({super.key, required this.title});

  final String title;
  final selectedColor = const Color.fromRGBO(249, 181, 12, 1);
  final unSelectedColor = const Color.fromRGBO(88, 47, 195, 1);

  @override
  State<Posts> createState() => _PostsState();
}

class _PostsState extends State<Posts> {
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
              TextButton.icon(
                onPressed: () async {
                  await API().logout();
                  Navigator.pushNamed(context, '/charts');
                },
                icon: const Icon(Icons.trending_up, size: 19),
                label: const Text("View Posting Trends",
                    style: TextStyle(fontSize: 16)),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: buildNavbar(
        selectedColor: widget.selectedColor,
        unSelectedColor: widget.unSelectedColor,
        currentPageIndex: 2,
        context: context,
      ),
    );
  }
}
