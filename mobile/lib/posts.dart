import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';
import 'api_interface.dart';
import 'utils.dart';

class Posts extends StatefulWidget {
  const Posts({super.key, required this.title});

  final String title;

  @override
  State<Posts> createState() => _PostsState();
}

class _PostsState extends State<Posts> {
  bool loadingPosts = true;
  List<dynamic> posts = [];

  void getData() async {
    loadingPosts = true;

    List<dynamic> postsData = (await API().getPosts()).data;

    for (final post in postsData) {
      post["time"] = DateTime.parse(post["time"]);
    }

    posts = postsData;

    setState(() {
      loadingPosts = false;
    });
  }

  Widget _itemBuilder(BuildContext context, int index) {
    return Card(
      child: Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          child: Column(
            children: [
              Text(
                posts[index]["title"],
                style: const TextStyle(fontSize: 20),
              ),
              Text(
                DateFormat.yMMMMd().add_jm().format(posts[index]["time"]),
                style: const TextStyle(fontSize: 15),
              ),
              Text(
                posts[index]["description"],
                style: const TextStyle(fontSize: 15),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    API().verify().then((value) => {
          if (value is Map)
            {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(value["error"]),
                ),
              ),
            }
        });

    if (loadingPosts == true) {
      getData();
    }

    return Scaffold(
      appBar: appbarComponent(title: widget.title),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(15, 20, 15, 0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              TextButton.icon(
                onPressed: () async {
                  if (context.mounted) context.go('/charts');
                },
                icon: const Icon(Icons.trending_up, size: 19),
                label: const Text(
                  "View Posting Trends",
                  style: TextStyle(fontSize: 16),
                ),
              ),
              loadingPosts
                  ? const CircularProgressIndicator(
                      color: Color.fromRGBO(100, 125, 155, 1),
                      strokeWidth: 3,
                    )
                  : posts.isEmpty
                      ? const Text('No Posts Yet! Add One!',
                          style: TextStyle(fontSize: 16))
                      : Expanded(
                          child: ListView.builder(
                            padding: const EdgeInsets.all(5.5),
                            itemCount: posts.length,
                            itemBuilder: _itemBuilder,
                          ),
                        ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: buildNavbar(
        currentPageIndex: 2,
        context: context,
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => {
          if (API().loggedIn())
            {context.go('/create-post')}
          else
            {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: RichText(
                    textAlign: TextAlign.center,
                    text: TextSpan(
                      style: const TextStyle(fontFamily: 'Nexa'),
                      children: [
                        const TextSpan(
                          text: 'Please ',
                          style: TextStyle(color: Colors.white),
                        ),
                        TextSpan(
                          text: 'login',
                          style: const TextStyle(
                            color: Colors.blue,
                            decoration: TextDecoration.underline,
                          ),
                          recognizer: TapGestureRecognizer()..onTap = () {
                              context.go('/authenticate');
                          },
                        ),
                        const TextSpan(
                          text: ' or ',
                          style: TextStyle(color: Colors.white),
                        ),
                        TextSpan(
                          text: 'register',
                          style: const TextStyle(
                            color: Colors.blue,
                            decoration: TextDecoration.underline,
                          ),
                          recognizer: TapGestureRecognizer()
                            ..onTap = () {
                              context.go('/authenticate');
                            },
                        ),
                        const TextSpan(
                          text: ' to create posts.',
                          style: TextStyle(color: Colors.white),
                        ),
                      ],
                    ),
                  ),
                ),
              )
            }
        },
        backgroundColor: const Color.fromRGBO(150, 125, 100, 1),
        child: const Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Icon(Icons.add, color: Colors.white),
            Text('Create Post',
                style: TextStyle(fontSize: 9, color: Colors.white),
                textAlign: TextAlign.center)
          ],
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.endTop,
    );
  }
}
