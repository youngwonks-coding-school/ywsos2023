import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'api_interface.dart';
import 'utils.dart';

class Profile extends StatefulWidget {
  const Profile({super.key, required this.title});

  final String title;

  @override
  State<Profile> createState() => _ProfileState();
}

class _ProfileState extends State<Profile> {
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
          padding: const EdgeInsets.fromLTRB(15, 40, 15, 0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              ElevatedButton.icon(
                onPressed: () async {
                  await API().logout();
                  if (context.mounted) context.go('/');
                },
                icon: const Icon(Icons.logout, size: 19),
                label: const Text("Sign Out", style: TextStyle(fontSize: 16)),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: buildNavbar(
        currentPageIndex: 3,
        context: context,
      ),
    );
  }
}
