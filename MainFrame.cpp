#include "MainFrame.h"
#include <wx/artprov.h>

MainFrame::MainFrame() : wxFrame(nullptr, wxID_ANY, "gui_ex_05_a",
                                    wxDefaultPosition, wxSize(500,400))
{
    m_fileMenu = new wxMenu;
    m_fileMenu->Append(wxID_OPEN, "&Open");
    m_fileMenu->Append(wxID_EXIT, "E&xit");

    m_testMenu = new wxMenu;
    m_testMenu->Append(ID_ADDMENU, "A&dd Menu");

    m_menubar = new wxMenuBar();
    m_menubar->Append(m_fileMenu, "&File");
    m_menubar->Append(m_testMenu, "&Test");

    SetMenuBar(m_menubar);

    Bind(wxEVT_MENU,
        &MainFrame::onExit,
        this,
        wxID_EXIT);

    CreateStatusBar();
    SetStatusText("Hello");

    m_toolbar = CreateToolBar();

    m_toolbar->AddTool(
        ID_OPEN,
        "Open",
        wxArtProvider::GetBitmap(wxART_FILE_OPEN));

    m_toolbar->Realize();

    Bind(wxEVT_TOOL,
        &MainFrame::onOpen,
        this,
        ID_OPEN);

    Bind(wxEVT_MENU,
        &MainFrame::onOpen,
        this,
        wxID_OPEN);

    Bind(wxEVT_MENU,
        &MainFrame::onAddMenu,
        this,
        ID_ADDMENU);
}

void MainFrame::onExit(wxCommandEvent&) {
    Close(true);
}

void MainFrame::onOpen(wxCommandEvent& ev) {
    wxMessageBox("Open Button Clicked");
}

void MainFrame::onAddMenu(wxCommandEvent& ev) {
    std::cout << "Adding Menu" << std::endl;
    m_testMenu->Append(
                ID_MENU1,
                "Menu1");

    Bind(wxEVT_MENU,
        &MainFrame::onMenu1,
        this,
        ID_MENU1);
}

void MainFrame::onMenu1(wxCommandEvent& ev) {
    std::cout << "Menu1" << std::endl;
    m_testMenu->Delete(ID_MENU1);
}
