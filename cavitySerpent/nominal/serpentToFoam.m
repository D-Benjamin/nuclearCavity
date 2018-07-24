% FUNCTION_NAME - Imports homogenized XS from Serpent to GeN-Foam
%
% Using the "<case>_res.m" output file from Serpent, this script generates the
% cross-section dictionaries to be used as input for GeN-Foam.
% The script can operate in interactive or automated more. During interactive
% mode, the necessary questions are interactively answered in order to generate
% 2 files: an answer script and GeN-Foam input. For an automated mode, the
% script is given a previously generated answers script in order to generate
% the GeN-Foam input autonomously.
%
% Author: Rodrigo Gonzalez Gonzaga de Oliveira, M.Sc., Nuclear Energy
% Paul Scherrer Institut, Laboratory for Advanced Nuclear Systems (ANS)
% email address: rodrigo.de-oliveira@psi.ch
%                rodrigoggoliveira@gmail.com
%
% Based on the original serpentToFoam by Carlo Fiorina
%
% Website: to be added after repo opens               <------
% June 2017; Last revision: 24-July-2018

%------------- BEGIN CODE --------------

function serpentToFoam

clear all % clearvars would be more suitable, but Octave does not support it yet.
clc

version = "24-July-2018";

% Constants
mev2j = 1.602176487e-13;
cm2m = 0.01;

%% Start data collection part

fprintf(['serpentToFoam - Version %s\n',...
    'This script generates XS dictionaries for neutronDiffusionFoam from a Serpent 2 output file (*_res.m ).\n',...
    'WARNING: use Octave!\n'],version);

fprintf(['\n',...
    'This script can be executed in 2 modes: interactive or automated.\n',...
    'Interactive mode will start a wizard to generate an answers script.\n',...
    'Automated mode will read all answers from a previously generated answers script.\n',...
    'If you would like to enter the interactive mode, type "i".\n',...
    'Otherwise, type the file name of an existing script (without extension).\n']);
selection = input('Select execution mode (i/file name): ','s');

% Generate a new script or load a previous one
if (strcmpi(selection,'i'))
    feval(interactiveMode);
else
    if exist(selection, 'file')
        fprintf(['\n',...
            'Reading answers script %s.m\n'],selection);
        feval(selection);
    else
        error('\nThe answers script %s.m file does not exist.\n',selection);
    end
end

% Load the Serpent output file
serpentOutput = strcat(serpentCase,'_res');
if exist(serpentOutput, 'file')
        fprintf(['\n',...
            'Reading Serpent output %s.m\n'],serpentOutput);
        run(serpentOutput);
else
        error('\nThe Serpent output %s.m file does not exist.\n',serpentOutput);
end

% Extract number or energy and delayed neutrons groups to size arrays
ng = MACRO_NG(idx); %number of energy groups
nd = length (FWD_ANA_BETA_ZERO)/2 -1; %number of delayed neutron precursors

% Name XS dictionary
switch (coreState)
    case 'N'
        foamDict = 'nominal';
    case 'C'
        foamDict = 'rhoCool';
    case 'CT'
        foamDict = 'TCool';
    case 'T'
        foamDict = 'TFuel';
    case 'CL'
        foamDict = 'expClad';
    case 'A'
        foamDict = 'expAxial';
    case 'R'
        foamDict = 'expRadial';
    otherwise
        error('Unrecognized core state.');
end

checkFileOverwrite('XS dictionary',foamDict);

%% Start creation of GeN-Foam input file

fprintf(['\n',...
    'Opening file %s\n'],foamDict);
fid=fopen(foamDict,'w');

% OpenFOAM solver general dictionary header
OFheader = sprintf([
    'FoamFile\n',...
    '{\n',...
    '    version     2.0;\n',...
    '    format      ascii;\n',...
    '    class       dictionary;\n',...
    '    location    "constant";\n',...
    '    object      %s;\n',...
    '}\n'],foamDict);
fprintf(fid, OFheader);

fprintf(fid,['\n',...
    '// Generated on %s\n',...
    '// by serpentToFoamXS version %s\n',...
    '// Data origin: %s\n'],date, version,serpentOutput);

fprintf(fid,'\n// delayed neutron spectrum: physical\n');
fprintf(fid,'// delayed neutron fraction: ');
if (strcmp(dnprec,'zero'))
    fprintf(fid,'physical');
else
    fprintf(fid,'effective');
end
fprintf(fid,'\n');

switch (coreState)
    case 'N'
        fprintf(fid,['\n',...
            'energyGroups    %i;\n',...
            'precGroups      %i;\n'],ng,nd);
    case 'C'
        fprintf(fid,['\n',...
            'rhoCoolRef %.6e;\n',...
            'rhoCoolPerturbed %.6e;\n'],...
            rhoCoolRef,rhoCoolPerturbed);
    case 'CT'
        fprintf(fid,['\n',...
            'TCoolRef %.6e;\n',...
            'TCoolPerturbed %.6e;\n'],...
            TCoolRef,TCoolPerturbed);
    case 'T'
        fprintf(fid,['\n',...
            'TfuelRef %.6e;\n',...
            'TfuelPerturbed %.6e;\n'],...
            TfuelRef,TfuelPerturbed);
    case 'CL'
        fprintf(fid,['\n',...
            'Tcladref %.6e;\n',...
            'TcladPerturbed %.6e;\n'],...
            Tcladref,TcladPerturbed);
    case 'A'
        fprintf(fid,['\n',...
            'expansionFromNominal %.6e;\n'],expansionFromNominalA);
    case 'R'
        fprintf(fid,['\n',...
            'expansionFromNominal %.6e;\n',...,);
            'radialOrientation %i %i %i;\n',...);
            'axialOrientation %i %i %i;\n'],...
            expansionFromNominalR,...
            radialOrientationX,radialOrientationY,radialOrientationZ,...
            AxialOrientationX,AxialOrientationY,AxialOrientationZ);
end

%% Create zones
fprintf(fid,['\n',...
    'zones\n',...
    '{\n']);

universeToZoneSize = (size(universeToZone));

%Loop over Universes we want to extract
for k=1:universeToZoneSize(1,1)

    %initialize search variables
    universeFound = false;

    universeToFind_universeName = universeToZone{k, 1};
    universeToFind_zoneName = universeToZone{k, 2};

    % Find the Universe number we want to extract inside Serpent output (GC_UNIVERSE_NAME)
    for i = 1:size(GC_UNIVERSE_NAME,1)
        if(strcmp(universeToFind_universeName,strcat(GC_UNIVERSE_NAME(i,:))))
            idx=i;
            universeFound = true;
        end
    end

    if (universeFound)

        fprintf(fid,[
        '    %s\n',...
        '    {\n'],universeToFind_zoneName);

        if (strcmp('N',coreState))
            % Inverse neutron speed (aka inverse velocity 1/V)
            IV = INF_INVV(idx,1:2:end) / cm2m;
            fprintf(fid,'        IV              nonuniform List<scalar> %i (%s );\n',...
            ng,sprintf(' %.6e',IV));

            % Prompt neutron spectrum
            XP = INF_CHIP(idx,1:2:end);
            fprintf(fid,'        chiPrompt       nonuniform List<scalar> %i (%s );\n',...
                ng,sprintf(' %.6e',XP));

            % Delayed neutron spectrum
            XD = INF_CHID(idx,1:2:end);
            % XD = XP;
            fprintf(fid,'        chiDelayed      nonuniform List<scalar> %i (%s );\n',...
                ng,sprintf(' %.6e',XD));

            % Discontinuity factors (needs further development)
            fprintf(fid,'        discFactor      nonuniform List<scalar> %i (',ng);
            for i = 1:ng
                    fprintf(fid,' 1');
            end
            fprintf(fid,' );\n');

            % Integral fluxes (needs further development)
            integralFlux = INF_FLX(idx,1:2:end) ./ INF_FLX(1,1:2:end);
            fprintf(fid,'        integralFlux    nonuniform List<scalar> %i (%s );\n\n',...
                ng,sprintf(' %.6e',integralFlux));

            % Delayed neutron precursors fraction (Beta)
            if (strcmp(dnprec,'zero'))
                beta = FWD_ANA_BETA_ZERO(idx,3:2:end);
            else
                beta = ADJ_IFP_ANA_BETA_EFF(idx,3:2:end);
            end

            fprintf(fid,'        beta            nonuniform List<scalar> %i (%s );\n',...
                nd,sprintf(' %.6e',beta));

            % Lambda (Delayed neutron precursors decay constants)
            if (strcmp(dnprec,'zero'))
                LAM = FWD_ANA_LAMBDA(idx,3:2:end);
            else
                LAM = ADJ_IFP_ANA_LAMBDA(idx,3:2:end);
            end

            fprintf(fid,'        lambda          nonuniform List<scalar> %i (%s );\n\n',...
                nd,sprintf(' %.6e',LAM));


        end

        % Diffusion coefficient
        D = INF_DIFFCOEF(idx,1:2:end) * cm2m;
        fprintf(fid,'        D               nonuniform List<scalar> %i (%s );\n',...
            ng,sprintf(' %.6e',D));

        % kappaFission
        kappaFission = ( INF_FISS(idx,1:2:end) .* INF_KAPPA(idx,1:2:end) ) / cm2m*mev2j;
        fprintf(fid,'        kappaFission    nonuniform List<scalar> %i (%s );\n',...
            ng,sprintf(' %.6e',kappaFission));

        % nuSigmaF
        NSF = INF_NSF(idx,1:2:end) / cm2m;
        fprintf(fid,'        nuSigmaF        nonuniform List<scalar> %i (%s );\n',...
            ng,sprintf(' %.6e',NSF));

        % Sigma removal (abs + capture + group transfer below)  obs:
        % actually total - diagonals of scattering production
        SP = INF_SP0(idx,1:2:end);

        REMXS = ( INF_TOT(idx,1:2:end) - SP(1:ng+1:end) ) / cm2m;
        fprintf(fid,'        sigmaRem        nonuniform List<scalar> %i (%s );\n',...
            ng,sprintf(' %.6e',REMXS));

        % Scattering matrix
        SM = reshape(SP, ng, ng);
        display(SM);
        SMstr = sprintf(['            (' repmat(' %.6e', 1, ng) ' )\n'], SM.' / cm2m);
        fprintf(fid,'        scatteringMatrix  %i  %i (\n%s        );\n',...
            ng,ng,SMstr);

        fprintf(fid,'    }\n');

    else
        error('Universe %s not found in Serpent universes.',universeToFind_universeName);

    end
end

fprintf(fid,'}\n');

fprintf(['\n',...
    'Saving file %s\n'],foamDict);
fclose(fid);

end

%% Interactive answers script generation!

% The function returns the name of the answers script, which will be used
% to generate the nuclearData dictionary

function newScript = interactiveMode

% Get a file name for the new script

newScript = input('\nEnter a file name for the answers script: ','s');

checkFileOverwrite('answers script',newScript);

%% Get a Serpent case

fprintf(['\n',...
    'Enter the Serpent case.\n',...
    'For example: enter "msfr_1" for a Serpent output "msfr_1_res.m".\n']);
while true
    serpentCase = input('File name: ', 's');
    serpentOutput = strcat(serpentCase,'_res');
    if exist(serpentOutput,'file')
        fprintf(['\n',...
            'Serpent output %s.m found!\n'],serpentOutput);
        run(serpentOutput);
        break
    else
        fprintf(['\n',...
            'The Serpent output %s.m file does not exist. Try again.\n'],serpentOutput);
    end
end

%% Selects physical or effective delayed neutron fraction and spectrum

fprintf(['\n',...
    'Treatment of delayed neutron: (2 options)\n',...
    'zero: Use the physical fractions and the delayed neutron spectrum.\n',...
    'eff: Use the effective fractions and the prompt neutron spectrum.\n']);
while true
    dnprec = input('zero or eff: ', 's');
    if strcmp(dnprec,'zero') || strcmp(dnprec,'eff')
        break
    else
        fprintf('\nInvalid treatment type! Please try again.\n');
    end
end

%% Finds the core state for the answer script

fprintf(['\n',...
    'What core state would you like the XS dictionary to be prepared for? (7 options)\n'...
    'N: Nominal core state\n'...
    'C: Expanded coolant\n'...
    'CT: Coolant temperature\n'...
    'T: Doppler broadened core\n'...
    'CL: Expanded cladding\n'...
    'A: Axially expanded core\n'...
    'R: Radially expanded core\n']);
while true
    coreState = input('Core state: ', 's');
    switch(coreState)
        case 'N'
            break
        case 'C'
            rhoCoolRef = getNumber('rhoCoolRef: ','Not a valid number! Re-enter rhoCoolRef: ');
            rhoCoolPerturbed = getNumber('rhoCoolPerturbed: ','Not a valid number! Re-enter rhoCoolPerturbed: ');
            break
        case 'CT'
            TCoolRef = getNumber('TCoolRef: ','Not a valid number! Re-enter TCoolRef: ');
            TCoolPerturbed = getNumber('TCoolPerturbed: ','Not a valid number! Re-enter TCoolPerturbed: ');
            break
        case 'T'
            TfuelRef = getNumber('TfuelRef: ','Not a valid number! Re-enter TfuelRef: ');
            TfuelPerturbed = getNumber('TfuelPerturbed: ','Not a valid number! Re-enter TfuelPerturbed: ');
            break
        case 'CL'
            Tcladref = getNumber('Tcladref: ','Not a valid number! Re-enter Tcladref: ');
            TcladPerturbed = getNumber('TcladPerturbed: ','Not a valid number! Re-enter TcladPerturbed: ');
            break
        case 'A'
            expansionFromNominalA = getNumber('Relative axial expansion compared to nominal: ',...
                'Not a valid number! Re-enter relative axial expansion: ');
            break
        case 'R'
            expansionFromNominalR = getNumber('Relative radial expansion compared to nominal: ',...
                'Not a valid number! Re-enter relative radial expansion: ');
            radialOrientationX = getNumber('Orientation of radial direction, x component: ',...
                'Not a valid number! Re-enter orientation of radial direction: ');
            radialOrientationY = getNumber('Orientation of radial direction, y component: ',...
                'Not a valid number! Re-enter orientation of radial direction: ');
            radialOrientationZ = getNumber('Orientation of radial direction, z component: ',...
                'Not a valid number! Re-enter orientation of radial direction: ');
            AxialOrientationX = getNumber('Orientation of Axial direction, x component: ',...
                'Not a valid number! Re-enter orientation of axial direction: ');
            AxialOrientationY = getNumber('Orientation of Axial direction, y component: ',...
                'Not a valid number! Re-enter orientation of axial direction: ');
            AxialOrientationZ = getNumber('Orientation of Axial direction, z component: ',...
                'Not a valid number! Re-enter orientation of axial direction: ');
            break
        otherwise
            fprintf('Invalid core state! Please try again.\n');
    end
end

%% Translate Serpent universes to GeN-Foam zones

serpentUniverses = cellstr(GC_UNIVERSE_NAME); % Using cells to handle string arrays is easier

fprintf(['\n',...
    'It is necessary to translate Serpent universes into zones for GeN-Foam.\n']);
universesAdded = 0;
while true
    universeFound = false;

    % Display information about what can be added and what was already
    fprintf(['\n',...
        'Valid universes to extract are:\n',...
        '\n',...
        '%s\n'],strjoin(serpentUniverses,'\n'));

    if universesAdded
       fprintf(['\n',...
           'The currently added universes are:\n',...
           ]);
       display(cell2table(universeToZone,...
           'VariableNames',{'universe' 'zone'}));
    end

    fprintf('\nEnter a universe to extract or "done" to finish\n')

    universeToExtract = input('universe or done: ','s');

    % check if extraction is done to break the loop or continue extraction
    if strcmp(universeToExtract,'done')
        break
    else
        % finds universe in Serpent output
        for i = 1:size(GC_UNIVERSE_NAME,1)
            if(strcmp(universeToExtract,strcat(GC_UNIVERSE_NAME(i,:))))
                fprintf('Universe found!\n');

                universeFound = true;
                universesAdded = universesAdded+1;

                zoneName = input('Enter a zone name: ','s');

                % stores the universe - zone
                universeToZone(universesAdded,(1:2)) = {universeToExtract, zoneName};
            end
        end

        if not (universeFound)
            fprintf('The universe is not valid!\n');
        end
    end
end

%% Print the answers script to a file

fprintf('Generating answers script.');
answersScript = fopen([newScript '.m'],'w');

fprintf(answersScript,[...
    'serpentCase = ' '''%s''' ';\n',...
    'dnprec = ' '''%s''' ';\n',...
    'coreState = ' '''%s''' ';\n'],...
    serpentCase,...
    dnprec,...
    coreState);


switch(coreState)
    case 'N'

    case 'C'
        fprintf(answersScript,[...
            'rhoCoolRef = %.6e;\n',...
            'rhoCoolPerturbed = %.6e;\n'],...
            rhoCoolRef,...
            rhoCoolPerturbed);
    case 'CT'
        fprintf(answersScript,[...
            'TCoolRef = %.6e;\n',...
            'TCoolPerturbed = %.6e;\n'],...
            TCoolRef,...
            TCoolPerturbed);
    case 'T'
        fprintf(answersScript,[...
            'TfuelRef = %.6e;\n',...
            'TfuelPerturbed = %.6e;\n'],...
            TfuelRef,...
            TfuelPerturbed);
    case 'CL'
        fprintf(answersScript,[...
            'Tcladref = %.6e;\n',...
            'TcladPerturbed = %.6e;\n'],...
            Tcladref,...
            TcladPerturbed);
    case 'A'
        fprintf(answersScript,[...
            'expansionFromNominalA = %.6e;\n'],...
            expansionFromNominalA);
    case 'R'
        fprintf(answersScript,[...
            'expansionFromNominalR = %.6e;\n',...
            'radialOrientationX = %i;\n',...
            'radialOrientationY = %i;\n',...
            'radialOrientationZ = %i;\n',...
            'AxialOrientationX = %i;\n',...
            'AxialOrientationY = %i;\n',...
            'AxialOrientationZ = %i;\n'],...
            expansionFromNominalR,...
            radialOrientationX,...
            radialOrientationY,...
            radialOrientationZ,...
            AxialOrientationX,...
            AxialOrientationY,...
            AxialOrientationZ);
end

fprintf(answersScript,['\n',...
    'universeToZone = {\n']);
for i = 1:size(universeToZone,1)
    fprintf(answersScript,[...
        '    ''' '%s' ''',''' '%s' ''';\n'],...
        universeToZone{i,1},...
        universeToZone{i,2});
end
fprintf(answersScript,'    };\n');

fclose(answersScript);

fprintf('The answers script was saved successfully.\n');

end

%% This function checks if the user wants to overwrite an existing file

%The function receives 2 strings as arguments:
%filetType indicates what kind of file it is (answers script or nuclearData
%   dictionary for example.
%fileName indicated the name of the file that will be checked for existance

%It doesn't return anything. If the user decides not to overwrite, it
%   throws an error instead.

function checkFileOverwrite(fileType,fileName)

if exist(fileName, 'file')
        fprintf(['\n',...
            'WARNING!\n',...
            'The %s file %s already exists.\n'],...
            fileType,fileName);
        while true
            overwrite = input('Would you like to overwrite it? (y/n): ', 's');
            switch(overwrite)
                case 'y'
                    break
                case 'n'
                    error('No file has been modified.');
                otherwise
                    fprintf('Invalid option.\n');
            end
        end
end

end

%% This function makes sure that the input is a number

%It receives 2 strings as arguments:
%msgOK to be displayed during normal input request
%msgNotOK to be displayed if the input is not a valid number

%It returns a number

function sureNumber = getNumber(msgOK,msgNotOK)

sureNumber = str2double(input(msgOK,'s'));
while isnan(sureNumber)
    sureNumber = str2double(input(msgNotOK,'s'));
end

end
