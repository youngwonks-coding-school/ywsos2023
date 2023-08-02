import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'api_interface.dart';
import 'utils.dart';

class CreatePost extends StatefulWidget {
  const CreatePost({super.key, required this.title});

  final String title;

  @override
  State<CreatePost> createState() => _CreatePostState();
}

class _CreatePostState extends State<CreatePost> {
  final titleController = TextEditingController();
  final descriptionController = TextEditingController();
  final locationController = TextEditingController();

  @override
  void dispose() {
    titleController.dispose();
    descriptionController.dispose();
    locationController.dispose();

    super.dispose();
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

    return Scaffold(
      appBar: appbarComponent(title: widget.title),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(15, 0, 15, 0),
          child: SingleChildScrollView(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: <Widget>[
                buildTextField(
                  labelText: "Title",
                  controller: titleController,
                  icon: Icons.title,
                  context: context,
                ),
                const SizedBox(height: 5),
                buildTextField(
                  labelText: "Description",
                  controller: descriptionController,
                  icon: Icons.description,
                  context: context,
                  multiline: true,
                ),
                const SizedBox(height: 5),
                buildTextField(
                  labelText: "Location",
                  controller: locationController,
                  icon: Icons.location_on,
                  context: context,
                ),
                const SizedBox(height: 5),
                ElevatedButton.icon(
                  onPressed: () async {
                    Response response = await API().createFoodBankPost(
                      title: titleController.text,
                      description: descriptionController.text,
                      location: locationController.text,
                    );

                    if (context.mounted) {
                      if (response.statusCode == 200) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('Successfully created post!'),
                          ),
                        );
                        context.go('/posts');
                      } else {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('Unable to create post!'),
                          ),
                        );
                      }
                    }
                  },
                  icon: const Icon(Icons.create, size: 19),
                  label: const Text("Create", style: TextStyle(fontSize: 16)),
                ),
              ],
            ),
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
