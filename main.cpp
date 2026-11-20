#include <iostream>
#include <stdio.h>
#include <wx/wx.h>
#include <wx/weakref.h>

#include "MainFrame.h"

// TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.

// int main(int nArgs, char* pArgs[]) {
//
//     printf("Hello, World\n");
//
//     return 0;
//     // TIP See CLion help at <a href="https://www.jetbrains.com/help/clion/">jetbrains.com/help/clion/</a>. Also, you can try interactive lessons for CLion by selecting 'Help | Learn IDE Features' from the main menu.
// }

class MyApp : public wxApp
{
public:
    bool OnInit() override
    {
        auto* frame = new MainFrame();
        frame->Show(true);

        return true;
    }
};

wxIMPLEMENT_APP(MyApp);