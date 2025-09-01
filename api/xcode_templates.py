XCODE_TEMPLATES = {
    "default": """
// Default Swift code snippet
import Foundation

print("Hello, World!")
""",
    "network": """
// Swift code for making a network request
import Foundation

guard let url = URL(string: "https://api.example.com/data") else {
    print("Invalid URL")
    return
}

let task = URLSession.shared.dataTask(with: url) { data, response, error in
    if let data = data {
        if let jsonString = String(data: data, encoding: .utf8) {
            print(jsonString)
        }
    } else if let error = error {
        print("HTTP Request Failed \\(error)")
    }
}

task.resume()
""",
    "ui": """
// Swift code for creating a simple UI with SwiftUI
import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack {
            Image(systemName: "globe")
                .imageScale(.large)
                .foregroundColor(.accentColor)
            Text("Hello, world!")
        }
    }
}
""",
    "table": """
// Swift code for creating a simple list with SwiftUI
import SwiftUI

struct ContentView: View {
    let data = ["Apple", "Banana", "Cherry", "Date"]

    var body: some View {
        List(data, id: \\.self) { item in
            Text(item)
        }
    }
}
"""
}
